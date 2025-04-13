from app import np, go, dash, dcc, html

dash.register_page(__name__, path="/predictions") 
layout = html.Div([
    html.H2("Future Electric Predictions"),

])
