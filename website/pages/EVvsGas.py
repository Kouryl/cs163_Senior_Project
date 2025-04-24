import os
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from app import get_csv_from_gcs  

dash.register_page(__name__, path="/EVvsGas")

# Constants for default efficiencies
DEFAULT_GAS_MPG = 25
DEFAULT_EV_MI_PER_KWH = 4

BUCKET_NAME = os.environ.get("BUCKET_NAME", "evernergy163.appspot.com")

# Load Data from GCS
gas_df = get_csv_from_gcs(BUCKET_NAME, 'data/Monthly Gas Prices.csv', header=3)
elec_df = get_csv_from_gcs(BUCKET_NAME, 'data/California Electric Rates.csv', header=0)
print("Gas DF loaded. Columns:", gas_df.columns.tolist())
print("Electric DF loaded. Columns:", elec_df.columns.tolist())

# Process Gas Prices Data
gas_df.columns = gas_df.columns.str.strip()
print("Before renaming, Gas DF columns:", gas_df.columns.tolist())
gas_df = gas_df.rename(columns={gas_df.columns[0]: 'Date', gas_df.columns[1]: 'Gas Price'})
print("After renaming, Gas DF columns:", gas_df.columns.tolist())

gas_df = gas_df[gas_df['Date'] != 'Date'].reset_index(drop=True)
gas_df['Gas Price'] = pd.to_numeric(gas_df['Gas Price'], errors='coerce')
gas_df['Date'] = pd.to_datetime(gas_df['Date'], format='%b-%Y', errors='coerce')
gas_df = gas_df.dropna(subset=['Date'])
gas_df = gas_df[(gas_df['Date'].dt.year >= 2000) & (gas_df['Date'].dt.year <= 2024)]
gas_df['YearMonth'] = gas_df['Date'].dt.to_period('M')
print("Processed Gas DF sample:")
print(gas_df.head())

# Process Electric Rates Data
elec_df.columns = elec_df.columns.str.strip()
print("Before renaming, Electric DF columns:", elec_df.columns.tolist())
if "Value (USD/kWh)" in elec_df.columns:
    elec_df = elec_df.rename(columns={"Value (USD/kWh)": "Electric Rate"})
elec_df['Date'] = pd.to_datetime(elec_df['Date'], errors='coerce')
elec_df = elec_df.dropna(subset=['Date'])
elec_df = elec_df[(elec_df['Date'].dt.year >= 2000) & (elec_df['Date'].dt.year <= 2024)]
elec_df['YearMonth'] = elec_df['Date'].dt.to_period('M')
print("Processed Electric DF sample:")
print(elec_df.head())

# Merge Datasets on YearMonth
merged_df = pd.merge(
    gas_df[['YearMonth', 'Gas Price', 'Date']],
    elec_df[['YearMonth', 'Electric Rate']],
    on='YearMonth'
)
print("Merged DF sample:")
print(merged_df.head())

# Analysis Calculations
corr = merged_df['Gas Price'].corr(merged_df['Electric Rate'])
merged_df['Gas Rate Change (%)'] = merged_df['Gas Price'].pct_change() * 100
merged_df['Electric Rate Change (%)'] = merged_df['Electric Rate'].pct_change() * 100
mean_gas_change = merged_df['Gas Rate Change (%)'].mean()
mean_elec_change = merged_df['Electric Rate Change (%)'].mean()
corr_rate = merged_df['Gas Rate Change (%)'].corr(merged_df['Electric Rate Change (%)'])
merged_df['Gas Cost per Mile'] = merged_df['Gas Price'] / DEFAULT_GAS_MPG
merged_df['EV Cost per Mile'] = merged_df['Electric Rate'] / DEFAULT_EV_MI_PER_KWH

# Create Plotly Figures
corr_fig = go.Figure(data=[
    go.Scatter(
        x=merged_df['Electric Rate'],
        y=merged_df['Gas Price'],
        mode='markers',
        name='Data Points',
        marker=dict(color='blue')
    )
])
corr_fig.update_layout(
    title="Correlation: Gas Price vs Electric Rate",
    xaxis=dict(title="Electric Rate ($/kWh)", showgrid=True, gridcolor='lightgrey', rangeslider=dict(visible=True)),
    yaxis=dict(title="Gas Price ($/Gallon)", showgrid=True, gridcolor='lightgrey'),
    template='plotly_white'
)

roc_fig = go.Figure(data=[
    go.Scatter(
        x=merged_df['Date'],
        y=merged_df['Gas Rate Change (%)'],
        mode='lines',
        name='Gas Rate Change (%)',
        line=dict(color='red')
    ),
    go.Scatter(
        x=merged_df['Date'],
        y=merged_df['Electric Rate Change (%)'],
        mode='lines',
        name='Electric Rate Change (%)',
        line=dict(color='blue')
    )
])
roc_fig.update_layout(
    title="Monthly Percentage Change in Gas and Electric Prices",
    xaxis=dict(showgrid=True, gridcolor='lightgrey'),
    yaxis=dict(showgrid=True, gridcolor='lightgrey'),
    template='plotly_white',
    updatemenus=[dict(
        type='buttons', direction='right', x=1.05, y=1.15, showactive=True,
        buttons=[
            dict(label='Both', method='restyle', args=[{'opacity': [1, 1]}]),
            dict(label='Gas Focus', method='restyle', args=[{'opacity': [1, 0.2]}]),
            dict(label='Electric Focus', method='restyle', args=[{'opacity': [0.2, 1]}]),
        ]
    )]
)

cost_fig = go.Figure(data=[
    go.Scatter(
        x=merged_df['Date'],
        y=merged_df['Gas Cost per Mile'],
        mode='lines',
        name='Gas Cost per Mile',
        line=dict(color='red')
    ),
    go.Scatter(
        x=merged_df['Date'],
        y=merged_df['EV Cost per Mile'],
        mode='lines',
        name='EV Cost per Mile',
        line=dict(color='orange', dash='dash')
    )
])
cost_fig.update_layout(
    title="Cost per Mile Comparison (Assumed Efficiencies)",
    xaxis=dict(showgrid=True, gridcolor='lightgrey'),
    yaxis=dict(showgrid=True, gridcolor='lightgrey'),
    template='plotly_white'
)

# Interactive Sensitivity Analysis Section
interactive_layout = html.Div([
    html.H4(
        "3. Interactive Sensitivity Analysis for Cost per Mile", 
        style={
            'marginLeft': '40px',
            'color': '#000000',
            'fontWeight': 'bold',
            'fontSize': '18px'
        }
    ),
    dcc.Markdown("""
    Adjust the sliders below to change the assumed vehicle efficiency for gas-powered cars (in MPG) 
    and electric vehicles (in miles per kWh). The cost per mile graph will update accordingly.
    """),
    html.Label("Gas Vehicle Efficiency (MPG):", style={
        'marginLeft': '40px',
        'color': '#000000',
        'fontWeight': 'bold'
    }),
    dcc.Slider(
        id="mpg-slider",
        min=10,
        max=50,
        step=1,
        value=DEFAULT_GAS_MPG,
        marks={n: str(n) for n in range(10, 51, 5)}
    ),
    html.Br(),
    html.Label("EV Efficiency (miles per kWh):", style={
        'marginLeft': '40px',
        'color': '#000000',
        'fontWeight': 'bold'
    }),
    dcc.Slider(
        id="mi-kwh-slider",
        min=2,
        max=10,
        step=0.1,
        value=DEFAULT_EV_MI_PER_KWH,
        marks={n: str(n) for n in range(2, 11)}
    ),
    html.Br(),
    dcc.Graph(id="interactive-cost-per-mile-graph")
], style={'margin': '20px'})

# Define the Final Dash Page Layout without try/except
layout = html.Div([
    html.H2('Major Findings for Electric vs Gasoline', style={'marginLeft': '20px'}),

    # Section 1: Correlation Analysis
    html.H4('1. Assessing the Long-Term Relationship Between Gas Prices and Electric Rates', style={
        'marginLeft': '40px',
        'color': '#000000',
        'fontWeight': 'bold',
        'fontSize': '18px'
    }),
    dcc.Markdown(f"""
Historical data shows a moderate positive correlation (r = {corr:.2f}) between gas prices and electric rates, suggesting that long-term trends in these energy prices tend to move together.
This correlation is statistically significant (p < 0.05), indicating that the relationship is unlikely to be due to random chance.
This supports the hypothesis that common economic forces such as inflation and commodity prices simultaneously affect both energy sources.
""", style={'marginLeft': '0px', 'marginRight': '20px'}),
    dcc.Graph(id="correlation-graph", figure=corr_fig, config={'scrollZoom': True, 'displayModeBar': True}),
    html.Br(),

    # Section 2: Cost per Mile Comparison (Static)
    html.H4('2. Cost per Mile for Gas-Powered and Electric Vehicles', style={
        'marginLeft': '40px',
        'color': '#000000',
        'fontWeight': 'bold',
        'fontSize': '18px'
    }),
    dcc.Markdown(f"""
Based on assumed fuel efficiencies (25 MPG for gas and 4 miles per kWh for EVs):

**Gas Cost per Mile:** ${merged_df['Gas Cost per Mile'].mean():.3f} per mile.  
**EV Cost per Mile:** ${merged_df['EV Cost per Mile'].mean():.3f} per mile.

This analysis demonstrates that EVs offer a significant operational cost advantage over gas vehicles.
""", style={'marginLeft': '0px', 'marginRight': '20px'}),
    dcc.Graph(id="cost-per-mile-graph", figure=cost_fig, 
              config={'modeBarButtonsToAdd': ['select2d', 'lasso2d'], 'scrollZoom': True}),
    html.Br(),

    # Section 2.5: Interactive Sensitivity Analysis
    interactive_layout,
    html.Br(),
    
    # Section 3: Monthly Rate of Change Analysis
    html.H4('4. Assessing Short-Term Volatility using Monthly Percentage Changes in Gas and Electric Prices', style={
        'marginLeft': '40px',
        'color': '#000000',
        'fontWeight': 'bold',
        'fontSize': '18px'
    }),
    dcc.Markdown(f"""
The analysis of monthly percentage changes reveals that gas and electric prices exhibit different short-term volatility patterns.

**Gas Price Rate Change:** {mean_gas_change:.2f}% per month.  
**Electric Rate Change:** {mean_elec_change:.2f}% per month.

The Pearson correlation between these changes is {corr_rate:.3f}, indicating that short-term fluctuations in gas and electric prices are nearly independent.

Despite the long-term interdependence, the short-term volatility in these markets is driven by different factors. 
This suggests that while both energy sources are affected by macroeconomic trends, their short-term price movements may be influenced by different market dynamics.
""", style={'marginLeft': '0px', 'marginRight': '20px'}),
    dcc.Graph(id="rate-change-graph", figure=roc_fig, config={'scrollZoom': True, 'displayModeBar': True}),
    html.Br(),

    # Section 4: Forecast Comparison and Projections (Next 5 Years)
    html.H4('5. Forecast Comparison and Projections (Next 5 Years)', style={
        'marginLeft': '40px',
        'color': '#000000',
        'fontWeight': 'bold',
        'fontSize': '18px'
    }),
    dcc.Markdown("""
Using Facebook Prophet models, we generated 5‑year forecasts for both gas prices and electric rates, incorporating seasonal effects and trend components. The combined comparison shows how both energy costs are expected to continue rising, with electric rates growing slightly faster seasonally. Individual plots include uncertainty intervals (shaded) to indicate confidence bounds, and a dashed vertical line marks the forecast start in 2025.
""", style={'marginLeft': '0px', 'marginRight': '20px','marginBottom': '10px'}),

    html.H4(
        "Forecast Comparison: Gas Prices vs Electric Rates (2025-2030)",
        style={
            'textAlign': 'center',
            'fontWeight': 'bold',
            'fontSize': '20px',
            'color': '#000000',
            'marginBottom': '20px'
        }
    ),
    
    # Combined Forecast Explanation Card
    html.Div([
        html.Img(
            src='https://storage.googleapis.com/evenergy163.appspot.com/results/forecast_comparison.png', 
            style={
                'width': '50%', 
                'height': 'auto', 
                'marginRight': '10px',
                'marginTop': '0px'
            }
        ),
        html.Div(
'''This combined forecast plot illustrates both historical and projected trajectories of gas prices (red) and electric rates (blue) spanning from 2000 to 2030. The dashed vertical line indicates the start of the 5-year forecast period (2025–2030). The forecast is generated using a time-series model (Facebook Prophet), which accounts for seasonal fluctuations and long-term trends in energy prices.

Observations:
• Gas prices exhibit clear seasonal peaks and troughs, typically aligning with consumer demand cycles.
• Electric rates display a more subtle but consistent upward trend, potentially tied to infrastructure costs and broader economic factors. 
• Over the next 5 years, both energy sources are projected to continue rising, with electric rates growing slightly faster. This could narrow the historical cost gap between electricity and gasoline in certain market conditions.
''',
            style={
                'textAlign': 'left', 
                'width': '50%', 
                'padding': '15px', 
                'border': '1px solid #ccc', 
                'borderRadius': '5px', 
                'backgroundColor': '#ffffff',
                'color': '#000000',
                'fontSize': '16px',
                'whiteSpace': 'pre-wrap',
                'margin': '0'
            }
        )
    ], style={
        'width': '80%',
        'margin': '0 auto',
        'marginBottom': '30px',
        'display': 'flex',
        'flexDirection': 'row',
        'alignItems': 'flex-start',
        'justifyContent': 'space-between'
    }),
    
    # Gas Forecast Explanation Card
    html.Div([
        html.H4(
            "Forecast for Gas Prices (2025–2030)",
            style={
                'textAlign': 'center',
                'fontWeight': 'bold',
                'fontSize': '20px',
                'color': '#000000',
                'marginBottom': '20px'
            }
        ),

        html.Div([
            html.Img(
                src='https://storage.googleapis.com/evenergy163.appspot.com/results/forecast_gas.png',
                style={
                    'width': '50%',
                    'height': 'auto',
                    'marginRight': '10px',
                    'marginTop': '0px'
                }
            ),
            html.Div(
"""The gas price forecast highlights seasonal peaks and long-term upward trends, with confidence intervals widening as the projection extends further. These intervals represent the model’s estimate of uncertainty, reflecting factors such as possible shifts in supply and demand, macroeconomic influences, or policy changes.

Observations:
• The Facebook Prophet model captures recurring annual patterns, shown by repeating peaks and troughs that often align with seasonal demand.
• An overall upward slope suggests that, barring major external shocks, gas prices may continue to rise steadily over the next 5 years.
• As the forecast extends farther from the most recent data point, uncertainty increases due to real-world unpredictability in markets, geopolitics, and technology shifts.
    """,
                style={
                    'textAlign': 'left',
                    'width': '50%',
                    'padding': '15px',
                    'border': '1px solid #ccc',
                    'borderRadius': '5px',
                    'backgroundColor': '#ffffff',
                    'color': '#000000',
                    'fontSize': '16px',
                    'whiteSpace': 'pre-wrap',
                    'margin': '0'
                }
            )
        ], style={
            'width': '80%',
            'margin': '0 auto',
            'marginBottom': '30px',
            'display': 'flex',
            'flexDirection': 'row',
            'alignItems': 'flex-start',
            'justifyContent': 'space-between'
        })
    ], style={'margin': '20px'}),
    
    # Electric Forecast Explanation Card
    html.Div([
        html.H4(
            'Forecast for Electric Rates (2025-2030)',
            style={
                'textAlign': 'center',
                'fontWeight': 'bold',
                'fontSize': '20px',
                'color': '#000000',
                'marginBottom': '20px'
            }
        ),

        html.Div([
            html.Img(
                src='https://storage.googleapis.com/evenergy163.appspot.com/results/forecast_electric.png',
                style={
                    'width': '50%',
                    'height': 'auto',
                    'marginRight': '10px',
                    'marginTop': '0px'
                }
            ),
            html.Div(
"""The electric rate forecast demonstrates a strong seasonal cycle and an overall growing trend, suggesting that electric costs may continue to rise steeply into 2030. Shaded confidence intervals (if shown) highlight the model’s uncertainty, indicating that rates could potentially deviate from this projection under different market conditions.

Observations:
• Electric demand often varies with climate, industrial cycles, and consumer usage; the model (Facebook Prophet) captures these ups and downs throughout each year.
• Overall upward trends may be driven by infrastructure investments, shifts toward electrification, and macroeconomic forces such as energy supply and commodity prices.
• Government incentives for renewable energy, grid modernization, and EV adoption can accelerate or alter electric rate patterns. Additionally, emerging technologies (e.g., battery storage) could stabilize or shift demand profiles.
    """,
                style={
                    'textAlign': 'left',
                    'width': '50%',
                    'padding': '15px',
                    'border': '1px solid #ccc',
                    'borderRadius': '5px',
                    'backgroundColor': '#ffffff',
                    'color': '#000000',
                    'fontSize': '16px',
                    'whiteSpace': 'pre-wrap',
                    'margin': '0'
                }
            )
        ], style={
            'width': '80%',
            'margin': '0 auto',
            'marginBottom': '30px',
            'display': 'flex',
            'flexDirection': 'row',
            'alignItems': 'flex-start',
            'justifyContent': 'space-between'
        })
    ], style={'margin': '20px'}),

    
    html.Br(),
    
    # Section 5: Overall Conclusions
    html.H3(
        'Overall Implications and Next Steps', 
        style={
            'marginLeft': '40px',
            'color': '#000000',
            'fontWeight': 'bold',
            'marginBottom': '0px',
            'fontSize': '20px'
        }
    ),
    html.Div(
        """ 
1. Long-term trends in gas and electric prices indicate common economic forces.
2. EVs offer a clear operational cost advantage based on cost per mile analysis.
3. Forecasts project continued price increases, with electric rates exhibiting stronger seasonal growth.
4. Uncertainty intervals highlight model confidence decreasing over time, underscoring the need for periodic recalibration.
        """,
        style={
            'whiteSpace': 'pre-wrap', 
            'color': '#000000',       
            'fontSize': '18px',
            'marginLeft': '40px',
            'marginRight': '20px',
            'marginTop': '3px',
            'marginBottom': '10px'
        }
    )
])
html.Br()


# Callback for interactive sensitivity analysis
@dash.callback(
    Output("interactive-cost-per-mile-graph", "figure"),
    [Input("mpg-slider", "value"), Input("mi-kwh-slider", "value")]
)
def update_interactive_cost_graph(mpg_value, mi_kwh_value):
    df = merged_df.copy()
    df["Gas Cost per Mile"] = df["Gas Price"] / mpg_value
    df["EV Cost per Mile"] = df["Electric Rate"] / mi_kwh_value
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Gas Cost per Mile"], mode="lines", name="Gas Cost per Mile"))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["EV Cost per Mile"], mode="lines", name="EV Cost per Mile", line=dict(dash="dash")))
    fig.update_layout(title="Interactive Sensitivity Analysis for Cost per Mile", xaxis_title="Date", yaxis_title="Cost per Mile (USD)", template="plotly_white")
    return fig
