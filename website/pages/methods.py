from app import np, go, dash, dcc, html

dash.register_page(__name__, path="/methods") 
layout = html.Div([
    html.H2("Analytical Methods"),
    html.P("For this project, the following analytical methods were used:"),
    html.P("1. Data Cleaning: We cleaned the data to ensure accuracy and consistency."),
    html.P("2. Data Visualization: We used various visualization techniques to present the data effectively."),
    html.P("3. Statistical Analysis: We performed statistical analysis to identify trends and patterns."),
    html.P("4. Predictive Modeling: We used machine learning algorithms to predict future energy consumption."),
    html.P("5. Cost Analysis: We compared the cost of charging an EV with the cost of gasoline."),
    html.P("6. Scenario Analysis: We conducted scenario analysis to understand the impact of different factors on energy consumption."),
    html.P("7. Sensitivity Analysis: We performed sensitivity analysis to identify the most influential factors on energy consumption."),
    html.P("8. Time Series Analysis: We used time series analysis to forecast future energy consumption trends."),
    html.P("9. Geographic Analysis: We analyzed the data geographically to understand regional differences in energy consumption."),
    html.P("10. Comparative Analysis: We compared the energy consumption of EVs with traditional vehicles."),
           
])
