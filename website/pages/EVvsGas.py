import os
import textwrap
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
interactive_layout = html.Div(
    className="interactive-section evvsgas-section",
    children=[
        html.H3(
            "3. Interactive Sensitivity Analysis for Cost per Mile",
            className="subsection-title"
        ),
        dcc.Markdown(
            """
Adjust the sliders below to change the assumed vehicle efficiency for gas-powered cars (in MPG) 
and electric vehicles (in miles per kWh). The cost per mile graph will update accordingly.
            """,
            className='full-width-text'
        ),

        html.Label("Gas Vehicle Efficiency (MPG):", className="label-text"),
        dcc.Slider(
            id="mpg-slider",
            min=10, max=50, step=1,
            value=DEFAULT_GAS_MPG,
            marks={n: str(n) for n in range(10, 51, 5)}
        ),
        html.Br(),

        html.Label("EV Efficiency (miles per kWh):", className="label-text"),
        dcc.Slider(
            id="mi-kwh-slider",
            min=2, max=10, step=0.1,
            value=DEFAULT_EV_MI_PER_KWH,
            marks={n: str(n) for n in range(2, 11)}
        ),
        html.Br(),

        # ← NEW: numeric readout of the current cost‐per‐mile values
        html.Div(
            id="interactive-cost-per-mile-values",
            style={
                'marginLeft': '40px',
                'marginBottom': '1rem',
                'fontSize': '1rem',
                'fontWeight': '600'
            }
        ),

        dcc.Graph(id="interactive-cost-per-mile-graph"),

        # your interpretation box remains unchanged
        html.Div(
            dcc.Markdown(
                """
**What You Can Explore:**  
Use the sliders to adjust assumed vehicle efficiency.  
- As gas MPG increases, the red line (gas cost/mile) falls.  
- As EV mi/kWh rises, the orange dashed line drops.  

In virtually all realistic efficiency ranges (10–50 MPG vs 2–10 mi/kWh), EVs remain cheaper per mile.  
This reinforces that even modest improvements in EV efficiency will further widen the cost gap.
                """
            ),
            className="interpretation"
        )
    ]
)

# Main Layout
layout = html.Div(className="page-container evvsgas-page", children=[

    html.H2(
    'Major Findings for Electric vs Gasoline',
    className='section-title',
    style={'marginTop': '5px', 'marginBottom': '20px'}
),
# Section 1
html.H3(
    '1. Long-Term Relationship: Gas Price vs Electric Rate',
    className='subsection-title'
),
dcc.Graph(
    id='correlation-graph',
    figure=corr_fig,
    className='chart-graph'
),

dcc.Markdown(f"""
Over the past **{len(merged_df)}** months, gas prices and electric rates have moved in tandem (unit-free correlation **r = {corr:.2f}**, moderately strong).

A correlation of **0.73** implies:
- **r² ≈ 0.53**, so about **53%** of one series’ month-to-month variation is linearly explained by the other.  
- The remaining **47%** comes from independent factors (weather, policy changes, local market effects).  
- With nearly **300** samples, the chance of seeing this by luck is effectively zero (**p ≪ 0.05**).

While this confirms both markets share common drivers (inflation, commodity costs), it **does not** tell us which is cheaper per mile.  
We’ll address that by converting to **cost per mile** in Section 2.
""", className='full-width-text callout'),

    # Section 2
    html.H3('2. Cost per Mile: Gas vs EV', className='subsection-title'),
    dcc.Markdown(f"""
    Based on assumed fuel efficiencies (25 MPG for gas and 4 miles per kWh for EVs):

    **Gas Cost per Mile:** ${merged_df['Gas Cost per Mile'].mean():.3f}  
    **EV Cost per Mile:** ${merged_df['EV Cost per Mile'].mean():.3f}  

    This analysis demonstrates that EVs offer a significant operational cost advantage over gas vehicles.
    """, className='full-width-text'),
    dcc.Graph(id='cost-per-mile-graph', figure=cost_fig, className='chart-graph'),
    dcc.Markdown(f"""
    **Key Takeaways:**  
    - **Gas Cost/Mile:** ${merged_df['Gas Cost per Mile'].mean():.3f}  
    - **EV Cost/Mile:** ${merged_df['EV Cost per Mile'].mean():.3f}  

    On average, driving an EV costs less than one-third as much per mile as a conventional car. This steady gap, shown in the red vs orange lines, highlights a clear operational advantage for EV ownership.
    """, className='interpretation'),

    # Interactive Section
    interactive_layout,

    # Section 4
    html.H3('4. Short-Term Volatility: Monthly % Changes', className='subsection-title'),
    dcc.Markdown(f"""
    The monthly percentage changes in gas prices and electric rates show a weak correlation (r = {corr_rate:.2f}), indicating that short-term fluctuations in these prices are largely independent. This suggests that while long-term trends may be related, short-term price movements are influenced by different factors.

    **Gas Rate Change:** {mean_gas_change:.2f}% per month  
    **Electric Rate Change:** {mean_elec_change:.2f}% per month  

    Pearson r = {corr_rate:.3f}, showing independent short-term moves.
    """, className='full-width-text'),
    dcc.Graph(id='rate-change-graph', figure=roc_fig, className='chart-graph'),
    dcc.Markdown(f"""
    **Short-Term Volatility Insights:**  
    Despite their long-term correlation, gasoline and electric rates behave quite differently month to month:  
    - **Gas Rate Change:** {mean_gas_change:.2f}% per month on average  
    - **Electric Rate Change:** {mean_elec_change:.2f}% per month  
    - **Monthly correlation:** r = {corr_rate:.2f}, essentially zero.  

    This tells us that short-run price swings are driven by distinct factors (weather, seasonal demand, supply disruptions).
    """, className='interpretation'),


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
The combined forecast shows gas prices (red) and electric rates (blue) rising through 2030, each with clear seasonal cycles.  
A dashed vertical line marks the start of the 5-year projection in 2025, after which the lines diverge more.

**Key points:**  
- Both fuels follow predictable annual ups and downs.  
- Electric rates are expected to climb a bit faster, narrowing the historical cost gap.  
- The widening confidence intervals remind us to refresh forecasts as markets evolve.
            """,
            className='full-width-text'
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
The gas price forecast shows clear annual peaks and a steady upward trend through 2030.  Confidence bands widen over time which shows that forecasts become less certain the further out we go.

**Key points:**  
- Seasonal spikes reflect predictable demand cycles (travel seasons, supply shifts).  
- The overall upward slope implies continued price pressure without major market disruptions.  
- Expanding confidence intervals underscore the importance of updating forecasts regularly.
            """,
            className='full-width-text'
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
The electric rate forecast shows clear annual peaks and an overall upward trend through 2030.  Shaded confidence bands widen over time which shows that these projections carry growing uncertainty.

**Key points:**  
- Seasonal swings reflect predictable demand cycles (weather, industrial activity).  
- A steady long-term rise likely stems from infrastructure costs and policy shifts.  
- Broad confidence intervals highlight the need to revisit and refine forecasts regularly.
            """,
            className='full-width-text'
        )
    ]),
    
        # ── 2024 Back‐Test Comparisons ──
    
    # ── Gas back‐test ──
html.H4('Gas Price Forecast vs Actual — 2024 Back-Test', className='subsection-title'),
html.Div(
    className='forecast-container',
    style={'display': 'flex', 'alignItems': 'flex-start', 'gap': '2rem'},
    children=[
        html.Img(
            src='https://storage.googleapis.com/evenergy163.appspot.com/results/download%20(71).png',
            className='forecast-image',
            style={'flex': '1 1 60%'}
        ),
        html.Ul(
            className='backtest-points',
            style={'flex': '1 1 40%', 'margin': 0, 'paddingLeft': '1rem'},
            children=[
                html.Li("Dashed red line generally overestimates actual gas prices, especially during summer months."),
                html.Li("Model captures spring rise but underestimates mid-year price dips caused by market shocks."),
                html.Li("MAE ≈ $0.55/gal (≈11% error) — acceptable for long-term budgeting but too coarse for monthly planning."),
            ]
        )
    ]
),
    
    # ── Electric back‐test ──
html.H4('Electric Rate Forecast vs Actual — 2024 Back-Test', className='subsection-title'),
html.Div(
    className='forecast-container',
    style={'display': 'flex', 'alignItems': 'flex-start', 'gap': '2rem'},
    children=[
        html.Img(
            src='https://storage.googleapis.com/evenergy163.appspot.com/results/download%20(72).png',
            className='forecast-image',
            style={'flex': '1 1 60%'}
        ),
        html.Ul(
            className='backtest-points',
            style={'flex': '1 1 40%', 'margin': 0, 'paddingLeft': '1rem'},
            children=[
                html.Li("Dashed red line closely follows the actual electric rates, with only small timing shifts."),
                html.Li("Model captures both the mid-year spike and late-year dip, though it smooths out some volatility."),
                html.Li("MAE ≈ $0.02/kWh (<8% error) — strong performance for both budget forecasting and operational planning."),
            ]
        )
    ]
),

    # Conclusions
    html.H3('Overall Takeaways & Next Steps', className='subsection-title'),
    html.Ul(className='conclusions-list', children=[
        html.Li(
            "Charging an EV runs about $0.04/mi versus $0.12/mi for a typical gasoline car, so you save roughly $0.08 each mile."
        ),
        html.Li(
            "Even under worst-case conditions (peak kWh rates, 10% charging losses, or low EV efficiency), EVs remain at least 50% cheaper per mile."
        ),
        html.Li(
            "Our 5-year forecasts show both gas prices and electric rates rising steadily through 2030, with electric rates climbing slightly faster—yet EVs retain their cost advantage per mile."
        ),
        html.Li(
            "Incorporate public-charger fees and regional rate structures to refine total operating-cost estimates."
        )
    ])
])

# Callback for interactive section
@dash.callback(
    Output("interactive-cost-per-mile-graph", "figure"),
    Output("interactive-cost-per-mile-values", "children"),
    [Input("mpg-slider", "value"), Input("mi-kwh-slider", "value")]
)
def update_interactive_cost_graph(mpg_value, mi_kwh_value):
    df = merged_df.copy()
    df["Gas Cost per Mile"] = df["Gas Price"] / mpg_value
    df["EV Cost per Mile"] = df["Electric Rate"] / mi_kwh_value

    # Update the figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["Gas Cost per Mile"],
        mode="lines", name="Gas Cost per Mile"
    ))
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["EV Cost per Mile"],
        mode="lines", name="EV Cost per Mile", line=dict(dash="dash")
    ))
    fig.update_layout(title="Interactive Cost per Mile", template="plotly_white")

    # Compute latest values for display
    latest = df.iloc[-1]
    date_str = latest["Date"].strftime("%b %Y")
    gas_val = latest["Gas Cost per Mile"]
    ev_val = latest["EV Cost per Mile"]
    text = f"{date_str} → Gas: ${gas_val:.3f}/mile  |  EV: ${ev_val:.3f}/mile"

    return fig, text