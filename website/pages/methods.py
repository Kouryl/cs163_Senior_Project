from app import np, go, dash, dcc, html

dash.register_page(__name__, path="/methods") 
layout = html.Div([
    html.H2("Analytical Methods"),
    html.P("We use a combination of data modeling and simulation techniques to analyze the effect of EVs on energy infrastructure. "
           "Our methods include grid modeling, demand forecasting, and scenario analysis.")
])
