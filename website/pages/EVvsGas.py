import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
from app import get_csv_from_gcs

dash.register_page(__name__, path="/EVvsGas")

# Load and Process the Data from GCS
BUCKET_NAME = os.environ.get("BUCKET_NAME", "evernergy163.appspot.com")
gas_df = get_csv_from_gcs(BUCKET_NAME, 'data/Monthly Gas Prices.csv')
elec_df = get_csv_from_gcs(BUCKET_NAME, 'data/California Electric Rates.csv')

# --- Process Gas Prices Data ---
if gas_df.columns[0] == "Unnamed: 0":
    gas_df = pd.read_csv(f"gs://{BUCKET_NAME}/data/Monthly Gas Prices.csv", skiprows=3, usecols=[0, 1])
    gas_df.columns = ['Date', 'Gas Price']

gas_df = gas_df[gas_df['Date'] != 'Date'].reset_index(drop=True)
gas_df['Gas Price'] = pd.to_numeric(gas_df['Gas Price'], errors='coerce')
gas_df['Date'] = pd.to_datetime(gas_df['Date'], format='%b-%Y', errors='coerce')
gas_df = gas_df.dropna(subset=['Date'])
gas_df = gas_df[(gas_df['Date'].dt.year >= 2000) & (gas_df['Date'].dt.year <= 2024)]
gas_df['YearMonth'] = gas_df['Date'].dt.to_period('M')

# --- Process Electric Rates Data ---
if "Value (USD/kWh)" in elec_df.columns:
    elec_df = elec_df.rename(columns={"Value (USD/kWh)": "Electric Rate"})
elec_df['Date'] = pd.to_datetime(elec_df['Date'], errors='coerce')
elec_df = elec_df.dropna(subset=['Date'])
elec_df = elec_df[(elec_df['Date'].dt.year >= 2000) & (elec_df['Date'].dt.year <= 2024)]
elec_df['YearMonth'] = elec_df['Date'].dt.to_period('M')

# --- Merge the Datasets on "YearMonth" ---
merged_df = pd.merge(
    gas_df[['YearMonth', 'Gas Price', 'Date']],
    elec_df[['YearMonth', 'Electric Rate']],
    on='YearMonth'
)

# Analysis Calculations

# 1. Long-Term Correlation Analysis
corr = merged_df[['Gas Price', 'Electric Rate']].corr().iloc[0, 1]

# 2. Monthly Rate of Change Analysis
merged_df['Gas Rate Change (%)'] = merged_df['Gas Price'].pct_change() * 100
merged_df['Electric Rate Change (%)'] = merged_df['Electric Rate'].pct_change() * 100
mean_gas_change = merged_df['Gas Rate Change (%)'].mean()
mean_elec_change = merged_df['Electric Rate Change (%)'].mean()
rate_changes = merged_df[['Gas Rate Change (%)', 'Electric Rate Change (%)']].dropna()
corr_rate = rate_changes['Gas Rate Change (%)'].corr(rate_changes['Electric Rate Change (%)'])

# 3. Cost per Mile Analysis
# Assumed efficiencies: 25 MPG for gas and 4 miles per kWh for EVs.
merged_df['Gas Cost per Mile'] = merged_df['Gas Price'] / 25
merged_df['EV Cost per Mile'] = merged_df['Electric Rate'] / 4

# -------------------------------
# Create Plotly Figures
# -------------------------------

# Figure 1: Correlation Graph (Scatter Plot)
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
    xaxis_title="Electric Rate ($/kWh)",
    yaxis_title="Gas Price ($/Gallon)",
    template="plotly_white"
)

# Figure 2: Monthly Rate of Change Graph
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
    xaxis_title="Date",
    yaxis_title="Percentage Change (%)",
    template="plotly_white"
)

# Figure 3: Cost per Mile Graph
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
    xaxis_title="Date",
    yaxis_title="Cost per Mile (USD)",
    template="plotly_white"
)


# Dash Page Layout
layout = html.Div([
    html.H2("Major Findings for Electric vs Gasoline"),
    html.H3("Analysis and Visualization:"),

    # Section 1: Correlation Analysis
    html.H4("1. Correlation Analysis"),
    dcc.Markdown(f"""
    **Summary:**  
    Historical data shows a moderate positive correlation (r = {corr:.2f}) between gas prices and electric rates, suggesting that long-term trends in these energy prices tend to move together.
    
    **Implications:**  
    This supports the hypothesis that common economic forces—such as inflation and commodity prices—simultaneously affect both energy sources.
    
    **Next Steps:**  
    Investigate causative factors further and incorporate additional market indicators.
    """),
    dcc.Graph(id='correlation-graph', figure=corr_fig),
    html.Br(),

    # Section 2: Cost per Mile Comparison
    html.H4("2. Cost per Mile Comparison"),
    dcc.Markdown(f"""
    **Summary:**  
    Based on assumed fuel efficiencies (25 MPG for gas and 4 miles per kWh for EVs):
    - **Gas Cost per Mile:** ${merged_df['Gas Cost per Mile'].mean():.3f} per mile.
    - **EV Cost per Mile:** ${merged_df['EV Cost per Mile'].mean():.3f} per mile.
    
    **Implications:**  
    This analysis demonstrates that EVs offer a significant operational cost advantage over gas vehicles.
    
    **Next Steps:**  
    Expand the analysis to include other costs (e.g., maintenance, total ownership) for a comprehensive evaluation.
    """),
    dcc.Graph(id='cost-per-mile-graph', figure=cost_fig),
    html.Br(),

    # Section 3: Monthly Rate of Change Analysis
    html.H4("3. Monthly Rate of Change Analysis"),
    dcc.Markdown(f"""
    **Summary:**  
    Analysis of monthly percentage changes reveals:
    - **Gas Price Rate Change:** {mean_gas_change:.2f}% per month.
    - **Electric Rate Change:** {mean_elec_change:.2f}% per month.
    
    The Pearson correlation between these changes is {corr_rate:.3f}, indicating that short-term fluctuations in gas and electric prices are nearly independent.
    
    **Implications:**  
    Despite long-term interdependence, the short-term volatility in these markets is driven by different factors.
    
    **Next Steps:**  
    Explore additional external variables and refine forecasting models for short-term price dynamics.
    """),
    dcc.Graph(id='rate-change-graph', figure=roc_fig),
    html.Br(),

    # Overall Conclusions and Next Steps
    html.H3("Overall Implications and Next Steps"),
    dcc.Markdown("""
    **Overall Conclusions:**  
    - Long-term trends in gas and electric prices indicate common economic forces.
    - EVs offer a clear operational cost advantage based on cost per mile analysis.
    - Short-term (monthly) price volatility appears largely independent between the two energy sources.
    
    **Next Steps:**  
    - Integrate additional variables (maintenance, total cost of ownership) for a more complete cost analysis.
    - Use advanced forecasting techniques to predict both long-term trends and short-term fluctuations.
    - Leverage these findings to support policy and investment decisions for sustainable transportation.
    """)
])
