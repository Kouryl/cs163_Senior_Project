import os
import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

from app import get_csv_from_gcs

dash.register_page(__name__, path="/EVvsGas")

# Constants
electrical_efficiency_kwh_per_mile = 4
gas_efficiency_mpg = 25
BUCKET_NAME = os.environ.get("BUCKET_NAME", "evernergy163.appspot.com")

# Load data
gas_df = get_csv_from_gcs(BUCKET_NAME, 'data/Monthly Gas Prices.csv', header=3)
elec_df = get_csv_from_gcs(BUCKET_NAME, 'data/California Electric Rates.csv', header=0)

# Process Gas Prices Data
gas_df.columns = gas_df.columns.str.strip()
gas_df = gas_df.rename(columns={gas_df.columns[0]: 'Date', gas_df.columns[1]: 'Gas Price'})
gas_df = gas_df[gas_df['Date'] != 'Date'].copy()
gas_df['Gas Price'] = pd.to_numeric(gas_df['Gas Price'], errors='coerce')
gas_df['Date'] = pd.to_datetime(gas_df['Date'], format='%b-%Y', errors='coerce')
gas_df = gas_df.dropna(subset=['Date'])
gas_df = gas_df[(gas_df['Date'].dt.year >= 2000) & (gas_df['Date'].dt.year <= 2024)]
gas_df['YearMonth'] = gas_df['Date'].dt.to_period('M')

# Process Electric Rates Data
elec_df.columns = elec_df.columns.str.strip()
elec_df = elec_df.rename(columns={'Value (USD/kWh)': 'Electric Rate'})
elec_df['Date'] = pd.to_datetime(elec_df['Date'], errors='coerce')
elec_df = elec_df.dropna(subset=['Date'])
elec_df = elec_df[(elec_df['Date'].dt.year >= 2000) & (elec_df['Date'].dt.year <= 2024)]
elec_df['YearMonth'] = elec_df['Date'].dt.to_period('M')

# Merge datasets on YearMonth
merged_df = pd.merge(
    gas_df[['YearMonth', 'Gas Price', 'Date']],
    elec_df[['YearMonth', 'Electric Rate']],
    on='YearMonth'
)

# Analysis
corr = merged_df['Gas Price'].corr(merged_df['Electric Rate'])
merged_df['Gas Rate Change (%)'] = merged_df['Gas Price'].pct_change() * 100
merged_df['Electric Rate Change (%)'] = merged_df['Electric Rate'].pct_change() * 100
mean_gas_change = merged_df['Gas Rate Change (%)'].mean()
mean_elec_change = merged_df['Electric Rate Change (%)'].mean()
corr_rate = merged_df['Gas Rate Change (%)'].corr(merged_df['Electric Rate Change (%)'])
merged_df['Gas Cost per Mile'] = merged_df['Gas Price'] / gas_efficiency_mpg
merged_df['EV Cost per Mile'] = merged_df['Electric Rate'] / electrical_efficiency_kwh_per_mile

# Figures with explicit grids and range slider
corr_fig = go.Figure(
    data=[go.Scatter(x=merged_df['Electric Rate'], y=merged_df['Gas Price'], mode='markers', name='Data Points')],
    layout=go.Layout(
        title='Correlation: Gas Price vs Electric Rate',
        xaxis=dict(
            title='Electric Rate ($/kWh)',
            showgrid=True,
            gridcolor='lightgrey',
            rangeslider=dict(visible=True)
        ),
        yaxis=dict(
            title='Gas Price ($/Gallon)',
            showgrid=True,
            gridcolor='lightgrey'
        ),
        template='plotly_white'
    )
)

roc_fig = go.Figure(
    data=[
        go.Scatter(x=merged_df['Date'], y=merged_df['Gas Rate Change (%)'], mode='lines', name='Gas Rate Change (%)'),
        go.Scatter(x=merged_df['Date'], y=merged_df['Electric Rate Change (%)'], mode='lines', name='Electric Rate Change (%)')
    ],
    layout=go.Layout(
        title='Monthly Percentage Change in Gas and Electric Prices',
        xaxis=dict(showgrid=True, gridcolor='lightgrey'),
        yaxis=dict(showgrid=True, gridcolor='lightgrey'),
        template='plotly_white'
    )
)

roc_fig.update_layout(
    updatemenus=[dict(
        type="buttons",
        direction="right",
        x=1.05,  # position to the right of the plot
        y=1.15,  # a little above the title
        showactive=True,
        buttons=[
            dict(
                label="Both",
                method="restyle",
                args=[{"opacity": [1, 1]}],  # both full strength
            ),
            dict(
                label="Gas Focus",
                method="restyle",
                args=[{"opacity": [1, 0.2]}],  # gas full, electric faded
            ),
            dict(
                label="Electric Focus",
                method="restyle",
                args=[{"opacity": [0.2, 1]}],  # gas faded, electric full
            ),
        ]
    )]
)

cost_fig = go.Figure(
    data=[
        go.Scatter(x=merged_df['Date'], y=merged_df['Gas Cost per Mile'], mode='lines', name='Gas Cost per Mile'),
        go.Scatter(x=merged_df['Date'], y=merged_df['EV Cost per Mile'], mode='lines', name='EV Cost per Mile', line=dict(dash='dash'))
    ],
    layout=go.Layout(
        title='Cost per Mile Comparison (Assumed Efficiencies)',
        xaxis=dict(showgrid=True, gridcolor='lightgrey'),
        yaxis=dict(showgrid=True, gridcolor='lightgrey'),
        template='plotly_white'
    )
)

# Dash layout
layout = html.Div([
    html.H2('Major Findings for Electric vs Gasoline', style={'marginLeft': '20px'}),
    html.H3('Analysis and Visualization:', style={'marginLeft': '20px'}),

    html.H4('1. Correlation Analysis', style={'marginLeft': '40px'}),
    html.Div(
        dcc.Markdown(
            f"""
**Summary:**  
Historical data shows a moderate positive correlation (r = {corr:.2f}) between gas prices and electric rates, suggesting that long-term trends in these energy prices tend to move together.

**Implications:**  
This supports the hypothesis that common economic forces—such as inflation and commodity prices—simultaneously affect both energy sources.
"""
        ),
        style={'marginLeft': '0px'}
    ),
    dcc.Graph(
        id='correlation-graph',
        figure=corr_fig,
        config={'scrollZoom': True, 'displayModeBar': True}
    ),
    html.Br(),

    html.H4('2. Cost per Mile Comparison', style={'marginLeft': '40px'}),
    html.Div([
        dcc.Markdown(
            """
**Summary:**  
Based on assumed fuel efficiencies (25 MPG for gas and 4 miles per kWh for EVs):
"""
        ),
        html.Ul([
            html.Li(f"Gas Cost per Mile: ${merged_df['Gas Cost per Mile'].mean():.3f} per mile."),
            html.Li(f"EV Cost per Mile: ${merged_df['EV Cost per Mile'].mean():.3f} per mile.")
        ], style={'marginLeft': '60px', 'paddingLeft': '0px', 'listStylePosition': 'inside'}),
        dcc.Markdown(
            """
**Implications:**  
This analysis demonstrates that EVs offer a significant operational cost advantage over gas vehicles.
"""
        )
    ], style={'marginLeft': '0px'}),
    dcc.Graph(
        id='cost-per-mile-graph',
        figure=cost_fig,
        config={'modeBarButtonsToAdd': ['select2d', 'lasso2d'], 'scrollZoom': True}
    ),
    html.Br(),

    html.H4('3. Monthly Rate of Change Analysis', style={'marginLeft': '40px'}),
    html.Div([
        dcc.Markdown(
            """
**Summary:**  
Analysis of monthly percentage changes reveals:
"""
        ),
        html.Ul([
            html.Li(f"Gas Price Rate Change: {mean_gas_change:.2f}% per month."),
            html.Li(f"Electric Rate Change: {mean_elec_change:.2f}% per month.")
        ], style={'marginLeft': '60px', 'paddingLeft': '0px', 'listStylePosition': 'inside'}),
        dcc.Markdown(
            f"""
The Pearson correlation between these changes is {corr_rate:.3f}, indicating that short-term fluctuations in gas and electric prices are nearly independent.

**Implications:**  
Despite long-term interdependence, the short-term volatility in these markets is driven by different factors.

**Next Steps:**  
Explore additional external variables and refine forecasting models for short-term price dynamics.
"""
        )
    ], style={'marginLeft': '0px'}),
    dcc.Graph(
        id='rate-change-graph',
        figure=roc_fig,
        config={'scrollZoom': True, 'displayModeBar': True}
    ),
    html.Br(),

    html.H3('Overall Implications and Next Steps', style={'marginLeft': '20px'}),
    html.Div(
        dcc.Markdown(
            """
**Overall Conclusions:**  
- Long-term trends in gas and electric prices indicate common economic forces.
- EVs offer a clear operational cost advantage based on cost per mile analysis.
- Short-term (monthly) price volatility appears largely independent between the two energy sources.
"""
        ),
        style={'marginLeft': '0px'}
    )
])
