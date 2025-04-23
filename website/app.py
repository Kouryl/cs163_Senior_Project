import dash
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import os
from dash import dcc, html
from dash.dependencies import Input, Output


from google.cloud import storage
from io import StringIO, BytesIO

def get_csv_from_gcs(bucket_name, source_blob_name, header=None):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    data = blob.download_as_text()
    return pd.read_csv(StringIO(data), header=header)

def get_xlsx_from_gcs(bucket_name, source_blob_name, header=None):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    data = blob.download_as_bytes()
    return pd.read_excel(BytesIO(data), header=header)

# Initialize the Dash app with pages support
app = dash.Dash(__name__, use_pages=True)
app.title = "CS 163 Project EV"
server = app.server

# Define the layout with a navigation bar using registered pages
app.layout = html.Div([
    html.Nav([
        dcc.Link("Home", href="/"),
        " | ",
        dcc.Link("Project Objective", href="/objective"),
        " | ",
        dcc.Link("Analytical Methods", href="/methods"),
        " | ",
        dcc.Link("EV Growth Findings", href="/findings"),
        " | ",
        dcc.Link("Electric vs Gasoline Findings", href="/EVvsGas"),
        " | ",
        dcc.Link("Future Predictions and Insights", href="/predictions"),
    ]),
    html.H1("EV Adoption Impact on the Energy Infrastructure"),
    
    # Automatically render the current page based on dash.page_registry
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True)
