# pages/home.py
from app import np, go, dash, dcc, html, px, go, os

dash.register_page(__name__, path="/") 

# Home page layout with a plot
layout = html.Div([
    html.H2("Welcome to the EV Impact on Energy Infrastructure"),
    html.P("This project explores the impact of electric vehicles on the energy infrastructure."),
    dcc.Graph(
        id='ev-impact-plot',
        figure={
            'data': [
                go.Scatter(
                    x=np.linspace(0, 10, 100),
                    y=np.sin(np.linspace(0, 10, 100)),
                    mode='lines',
                    name='Sine Wave'
                )
            ],
            'layout': go.Layout(
                title='Sine Wave Plot',
                xaxis={'title': 'Time'},
                yaxis={'title': 'Amplitude'}
            )
        }
    )
])
