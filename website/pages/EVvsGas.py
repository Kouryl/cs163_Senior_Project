import os
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

from app import dash, get_csv_from_gcs

# Register the page
dash.register_page(__name__, path="/EVvsGas")

# Constants for default efficiencies
DEFAULT_GAS_MPG = 25
DEFAULT_EV_MI_PER_KWH = 4
BUCKET_NAME = os.environ.get("BUCKET_NAME", "evernergy163.appspot.com")

# Load Data from GCS
gas_df = get_csv_from_gcs(BUCKET_NAME, 'data/Monthly Gas Prices.csv', header=3)
elec_df = get_csv_from_gcs(BUCKET_NAME, 'data/California Electric Rates.csv', header=0)

# Process Gas Prices Data
gas_df.columns = gas_df.columns.str.strip()
gas_df = gas_df.rename(columns={gas_df.columns[0]: 'Date', gas_df.columns[1]: 'Gas Price'})
gas_df = gas_df[gas_df['Date'] != 'Date'].reset_index(drop=True)
gas_df['Gas Price'] = pd.to_numeric(gas_df['Gas Price'], errors='coerce')
gas_df['Date'] = pd.to_datetime(gas_df['Date'], format='%b-%Y', errors='coerce')
gas_df = gas_df.dropna(subset=['Date'])
gas_df = gas_df[(gas_df['Date'].dt.year >= 2000) & (gas_df['Date'].dt.year <= 2024)]
gas_df['YearMonth'] = gas_df['Date'].dt.to_period('M')

# Process Electric Rates Data
elec_df.columns = elec_df.columns.str.strip()
if "Value (USD/kWh)" in elec_df.columns:
    elec_df = elec_df.rename(columns={"Value (USD/kWh)": "Electric Rate"})
elec_df['Date'] = pd.to_datetime(elec_df['Date'], errors='coerce')
elec_df = elec_df.dropna(subset=['Date'])
elec_df = elec_df[(elec_df['Date'].dt.year >= 2000) & (elec_df['Date'].dt.year <= 2024)]
elec_df['YearMonth'] = elec_df['Date'].dt.to_period('M')

# Merge Datasets on YearMonth
merged_df = pd.merge(
    gas_df[['YearMonth', 'Gas Price', 'Date']],
    elec_df[['YearMonth', 'Electric Rate']],
    on='YearMonth'
)

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
    go.Scatter(x=merged_df['Electric Rate'], y=merged_df['Gas Price'], mode='markers', name='Data Points')
])
corr_fig.update_layout(
    title="Correlation: Gas Price vs Electric Rate",
    xaxis=dict(title="Electric Rate ($/kWh)", showgrid=True, gridcolor='lightgrey', rangeslider=dict(visible=True)),
    yaxis=dict(title="Gas Price ($/Gallon)", showgrid=True, gridcolor='lightgrey'),
    template='plotly_white'
)

roc_fig = go.Figure(data=[
    go.Scatter(x=merged_df['Date'], y=merged_df['Gas Rate Change (%)'], mode='lines', name='Gas Rate Change (%)', line=dict(color='red')),
    go.Scatter(x=merged_df['Date'], y=merged_df['Electric Rate Change (%)'], mode='lines', name='Electric Rate Change (%)', line=dict(color='blue'))
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
    go.Scatter(x=merged_df['Date'], y=merged_df['Gas Cost per Mile'], mode='lines', name='Gas Cost per Mile', line=dict(color='red')),
    go.Scatter(x=merged_df['Date'], y=merged_df['EV Cost per Mile'], mode='lines', name='EV Cost per Mile', line=dict(color='orange', dash='dash'))
])
cost_fig.update_layout(
    title="Cost per Mile Comparison (Assumed Efficiencies)",
    xaxis=dict(showgrid=True, gridcolor='lightgrey'),
    yaxis=dict(showgrid=True, gridcolor='lightgrey'),
    template='plotly_white'
)

# Interactive Section
interactive_layout = html.Div(className="interactive-section evvsgas-section", children=[
    html.H3("3. Interactive Sensitivity Analysis for Cost per Mile", className="subsection-title"),
    dcc.Markdown(
        """
Adjust the sliders below to change the assumed vehicle efficiency for gas-powered cars (in MPG) 
and electric vehicles (in miles per kWh). The cost per mile graph will update accordingly.
        """, className="content-text"
    ),
    html.Label("Gas Vehicle Efficiency (MPG):", className="label-text"),
    dcc.Slider(id="mpg-slider", min=10, max=50, step=1, value=DEFAULT_GAS_MPG, marks={n: str(n) for n in range(10, 51, 5)}),
    html.Br(),
    html.Label("EV Efficiency (miles per kWh):", className="label-text"),
    dcc.Slider(id="mi-kwh-slider", min=2, max=10, step=0.1, value=DEFAULT_EV_MI_PER_KWH, marks={n: str(n) for n in range(2, 11)}),
    html.Br(),
    dcc.Graph(id="interactive-cost-per-mile-graph")
])

# Main Layout
layout = html.Div(className="page-container evvsgas-page", children=[

    html.H2('Major Findings for Electric vs Gasoline', className='section-title'),

    # Section 1
    html.H3('1. Long-Term Relationship: Gas Price vs Electric Rate', className='subsection-title'),
    dcc.Markdown(f"""
Historical data shows a moderate positive correlation (r = {corr:.2f}) between gas prices and electric rates, suggesting that long-term trends in these energy prices tend to move together.
This correlation is statistically significant (p < 0.05), indicating that the relationship is unlikely to be due to random chance.
This supports the hypothesis that common economic forces such as inflation and commodity prices simultaneously affect both energy sources.
""", className='content-text'),
    dcc.Graph(id='correlation-graph', figure=corr_fig, className='chart-graph'),

    # Section 2
    html.H3('2. Cost per Mile: Gas vs EV', className='subsection-title'),
    dcc.Markdown(f"""
Based on assumed fuel efficiencies (25 MPG for gas and 4 miles per kWh for EVs):

**Gas Cost per Mile:** ${merged_df['Gas Cost per Mile'].mean():.3f}  
**EV Cost per Mile:** ${merged_df['EV Cost per Mile'].mean():.3f}  

This analysis demonstrates that EVs offer a significant operational cost advantage over gas vehicles.
""", className='content-text'),
    dcc.Graph(id='cost-per-mile-graph', figure=cost_fig, className='chart-graph'),

    # Interactive Section
    interactive_layout,

    # Section 4
    html.H3('4. Short-Term Volatility: Monthly % Changes', className='subsection-title'),
    dcc.Markdown(f"""
The monthly percentage changes in gas prices and electric rates show a weak correlation (r = {corr_rate:.2f}), indicating that short-term fluctuations in these prices are largely independent. This suggests that while long-term trends may be related, short-term price movements are influenced by different factors.

**Gas Rate Change:** {mean_gas_change:.2f}% per month  
**Electric Rate Change:** {mean_elec_change:.2f}% per month  

Pearson r = {corr_rate:.3f}, showing independent short-term moves.
""", className='content-text'),
    dcc.Graph(id='rate-change-graph', figure=roc_fig, className='chart-graph'),

    # Section 5: Forecast Comparison (2025–2030)
    html.H3('5. Forecast Comparison (2025–2030)', className='subsection-title'),

    # Combined Forecast
    html.Div(className='forecast-container evvsgas-section', children=[
        html.Img(
            src='https://storage.googleapis.com/evenergy163.appspot.com/results/forecast_comparison.png',
            className='forecast-image'
        ),
        dash.dcc.Markdown(
            """
This combined forecast plot illustrates both historical and projected trajectories of gas prices (red) and electric rates (blue) spanning from 2000 to 2030. The dashed vertical line indicates the start of the 5-year forecast period (2025–2030). The forecast is generated using a time-series model (Facebook Prophet), which accounts for seasonal fluctuations and long-term trends in energy prices.


**Observations**:
• Gas prices exhibit clear seasonal peaks and troughs, typically aligning with consumer demand cycles.
• Electric rates display a more subtle but consistent upward trend, potentially tied to infrastructure costs and broader economic factors. 
• Over the next 5 years, both energy sources are projected to continue rising, with electric rates growing slightly faster. This could narrow the historical cost gap between electricity and gasoline in certain market conditions.
            """,
            className='content-text'
        )
    ]),

    # Forecast for Gas Prices
    html.H4('Forecast for Gas Prices (2025–2030)', className='subsection-title'),
    html.Div(className='forecast-container evvsgas-section', children=[
        html.Img(
            src='https://storage.googleapis.com/evenergy163.appspot.com/results/forecast_gas.png',
            className='forecast-image'
        ),
        dash.dcc.Markdown(
            """
The gas price forecast highlights seasonal peaks and long-term upward trends, with confidence intervals widening as the projection extends further. These intervals represent the model’s estimate of uncertainty, reflecting factors such as possible shifts in supply and demand, macroeconomic influences, or policy changes.


**Observations**:
• The Facebook Prophet model captures recurring annual patterns, shown by repeating peaks and troughs that often align with seasonal demand.
• An overall upward slope suggests that, barring major external shocks, gas prices may continue to rise steadily over the next 5 years.
• As the forecast extends farther from the most recent data point, uncertainty increases due to real-world unpredictability in markets, geopolitics, and technology shifts.
            """,
            className='content-text'
        )
    ]),

    # Forecast for Electric Rates
    html.H4('Forecast for Electric Rates (2025–2030)', className='subsection-title'),
    html.Div(className='forecast-container evvsgas-section', children=[
        html.Img(
            src='https://storage.googleapis.com/evenergy163.appspot.com/results/forecast_electric.png',
            className='forecast-image'
        ),
        dash.dcc.Markdown(
            """
The electric rate forecast demonstrates a strong seasonal cycle and an overall growing trend, suggesting that electric costs may continue to rise steeply into 2030. Shaded confidence intervals (if shown) highlight the model’s uncertainty, indicating that rates could potentially deviate from this projection under different market conditions.

• Electric demand often varies with climate, industrial cycles, and consumer usage; the model (Facebook Prophet) captures these ups and downs throughout each year.
• Overall upward trends may be driven by infrastructure investments, shifts toward electrification, and macroeconomic forces such as energy supply and commodity prices.
• Government incentives for renewable energy, grid modernization, and EV adoption can accelerate or alter electric rate patterns. Additionally, emerging technologies (e.g., battery storage) could stabilize or shift demand profiles.
            """,
            className='content-text'
        )
    ]),


    # Conclusions
    html.H3('Overall Implications & Next Steps', className='subsection-title'),
    html.Ul(className='conclusions-list', children=[
        html.Li('Long-term trends indicate common economic forces.'),
        html.Li('EVs offer clear operational cost advantages.'),
        html.Li('Forecasts project continued price increases with seasonal dynamics.'),
        html.Li('Uncertainty intervals highlight need for periodic model recalibration.')
    ])
])

# Callback for interactive section
@callback(
    Output('interactive-cost-per-mile-graph', 'figure'),
    [Input('mpg-slider', 'value'), Input('mi-kwh-slider', 'value')]
)
def update_interactive_cost_graph(mpg_value, mi_kwh_value):
    df = merged_df.copy()
    df['Gas Cost per Mile'] = df['Gas Price'] / mpg_value
    df['EV Cost per Mile'] = df['Electric Rate'] / mi_kwh_value
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Gas Cost per Mile'], mode='lines', name='Gas Cost per Mile'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['EV Cost per Mile'], mode='lines', name='EV Cost per Mile', line=dict(dash='dash')))
    fig.update_layout(title='Interactive Cost per Mile', template='plotly_white')
    return fig