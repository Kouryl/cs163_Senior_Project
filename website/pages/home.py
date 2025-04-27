# pages/home.py
import dash
from dash import html, dcc

dash.register_page(__name__, path="/")

layout = html.Div(className="page-container", children=[

    # 1) Page Title (only H1)
    html.H1(
        "EV Adoption Impact on the Energy Infrastructure",
        className="home-main-title"
    ),

    # 2) Hero Section (video + overlay)
    html.Div(className="hero-section", children=[
        # 2a) background video
        html.Video(
            src="https://storage.googleapis.com/evenergy163.appspot.com/video/Complete%20Video.mp4", # https://storage.googleapis.com/evenergy163.appspot.com/video/Complete%20Video.mp4
            autoPlay=True,
            muted=True,
            loop=True,
            className="hero-video"
        ),

        # 2b) overlay: subtitle + button
        html.Div(className="hero-overlay", children=[
            html.H2("Discover EV Adoption Trends", className="hero-title"),
            html.P("See how EV growth is reshaping our energy grid", className="hero-subtitle"),
            html.A("Explore Insights", href="/objective", className="hero-cta")
        ]),
    ]),

    # 3) Cards Section (Project Overview + Broader Impacts)
    html.Div(className="cards-container", children=[
        html.Div(className="card-panel", children=[
            html.H2("Project Overview", className="card-title"),
            html.Div(
                "The adoption of electric vehicles (EVs) plays a crucial role in the transition toward sustainable "
                "transportation. In this project, we aim to examine the EV adoption trends in the Pacific Region, focusing "
                "on growth patterns, geographic distribution, vehicle characteristics, and predictive "
                "modeling to understand future adoption trends and their impact on the energy grid. Additionally, we will "
                "also be exploring whether the cost of charging EVs is economically viable to replace gasoline-powered vehicles.",
                className="card-text",
                style={'marginLeft': '0px', 'marginRight': '20px'}
            )
        ]),

        html.Div(className="card-panel",
            style={'backgroundColor': '#e0e0e0'},
            children=[
            html.H2("Broader Impacts", className="card-title"),
            html.Div(
                "Understanding EV adoption helps policymakers and environmental groups assess the extent to which EVs "
                "reduce carbon emissions and evaluate the effectiveness of clean energy policies and incentives. "
                "Identifying areas with high EV adoption provides insight into where environmental benefits such as "
                "reduced air pollution are most concentrated and where further efforts may be needed.",
                className="card-text",
                style={'marginLeft': '0px', 'marginRight': '20px'}
            )
        ]),
    ])
])
