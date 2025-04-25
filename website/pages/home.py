# pages/home.py
import dash
from dash import html, dcc

dash.register_page(__name__, path="/")

layout = html.Div([
    # Hero Video Section
      html.Div([
    # 1a) video background
        html.Video(
        src="https://storage.googleapis.com/evenergy163.appspot.com/video/videoplayback.webm",
        autoPlay=True, muted=True, loop=True,
        className="hero-video"
        ),

        # 1b) overlay + text/button all in the same container
        html.Div([
        html.H1("Discover EV Adoption Trends", className="hero-title"),
        html.P("See how EV growth is reshaping our energy grid", className="hero-subtitle"),
        html.A("Explore Insights", href="/EVvsGas", className="hero-cta")
        ], className="hero-overlay")
    ], className="hero-section"),

    # Cards Section (unchanged)
    html.Div([
        html.Div([
            html.H2("Project Overview", className="card-title"),
            html.P(
                "The adoption of electric vehicles (EVs) plays a crucial role in the transition toward sustainable transportation. "
                "This project examines EV adoption trends in the Pacific Region and compares EV charging costs vs gasoline.",
                className="card-text"
            )
        ], className="card-panel"),

        html.Div([
            html.H2("Broader Impacts", className="card-title"),
            html.P(
                "Understanding EV adoption helps policymakers assess carbon emission reductions and evaluate clean energy policies.",
                className="card-text"
            )
        ], className="card-panel")
    ], className="cards-container")
], className="page-container")
