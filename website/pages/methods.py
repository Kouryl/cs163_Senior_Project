from app import np, go, dash, dcc, html

dash.register_page(__name__, path="/methods") 
layout = html.Div([
    html.H2("Analytical Methods"),
    html.P("For this project, the following analytical methods were used:"),
    html.P("1. Time series Aggregation: grouping charging session and energy usage by month to analyze trends."),
    html.P("2. Line plots: used to display growth of sessions and energy delivered over time."),
    html.P("3. Heatmaps: used to visualize charging activty by area and month to identify popular areas in the pacific region."),
    html.P("4. Descriptive Statistics: comparing mean and median values to access data skew and represent typical user behaviors."),
    html.P("5. Cost Analysis: We compared the cost of charging an EV with the cost of gasoline."),
    html.P("6. Geographic Analysis: We analyzed the data geographically to understand regional differences in energy consumption."),
])
