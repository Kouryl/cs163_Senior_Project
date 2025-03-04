import dash
import importlib
import pandas as pd
import plotly.express as px
import os
from dash import dcc, html
from dash.dependencies import Input, Output
from google.cloud import storage
from io import StringIO

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "CS 163 Project EV"
server = app.server

# Define the layout with a constant navigation bar
app.layout = html.Div([
    html.Nav([
        dcc.Link("Home", href="/"),
        " | ",
        dcc.Link("Project Objective", href="/objective"),
        " | ",
        dcc.Link("Analytical Methods", href="/methods"),
        " | ",
        dcc.Link("Major Findings", href="/findings"),
    ]),
    html.H1("EV Impact on Energy Infrastructure"),
    dcc.Location(id='url', refresh=False),  # This will track the current URL
    html.Div(id='page-content')  # This will display the content based on the URL
])

# Define the callback to update page content based on the URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    # Define the mapping of URL paths to pages
    pages = {
        '/': 'home',
        '/objective': 'objective',
        '/methods': 'methods',
        '/findings': 'findings'
    }

    if pathname in pages:
        # Dynamically import the correct page
        page_module = importlib.import_module(f'pages.{pages[pathname]}')
        return page_module.layout
    else:
        return html.H2("404 - Page Not Found")

if __name__ == '__main__':
    app.run_server(debug=True)
