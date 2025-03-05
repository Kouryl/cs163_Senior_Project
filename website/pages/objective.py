from app import np, go, dash, dcc, html

dash.register_page(__name__, path="/objective") 

layout = html.Div([
    html.H2("Project Objective"),
    html.P("This project aims to analyze the impact of electric vehicles (EVs) on energy infrastructure. "
           "We focus on understanding the adoption rate, charging requirements, and grid demand shifts.")
])
