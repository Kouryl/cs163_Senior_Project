# pages/home.py
import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div(className="page-container", children=[

    html.H1(
        "EV Growth and Its Effect on Charging Demand",
        className="home-main-title"
    ),

    html.Div(className="hero-section", children=[
        html.Video(
            src="https://storage.googleapis.com/evenergy163.appspot.com/video/Complete%20Video.mp4",  # https://storage.googleapis.com/evenergy163.appspot.com/video/Complete%20Video.mp4
            autoPlay=True, muted=True, loop=True,
            className="hero-video"
        ),
        html.Div(className="hero-overlay", children=[
            html.H2("Discover EV Adoption Trends", className="hero-title"),
            html.P("See how EV growth is reshaping our energy grid", className="hero-subtitle"),
            html.A("Explore Insights", href="/objective", className="hero-cta")
        ]),
    ]),

    html.Div(className="cards-container", children=[

        # Project Overview
        html.Div(className="card-panel", children=[
            html.H2("Project Overview", className="card-title"),
            html.Div(
                "The adoption of electric vehicles (EVs) plays a crucial role in the transition toward sustainable transportation. "
                "In this project, we analyzed EV charging sessions and kWh delivered across the Pacific Region to identify growth patterns, "
                "geographic hotspots, and key vehicle characteristics. We then translated historical energy and gasoline prices into a common "
                "cost-per-mile metric—allowing a direct comparison of EV charging vs. fuel costs—and built 5-year time-series forecasts to "
                "project future demand on the energy grid.",
                className="card-text"
            )
        ]),

        # Broader Impacts
        html.Div(className="card-panel", children=[
            html.H2("Broader Impacts", className="card-title"),
            html.Div(
                "Understanding EV adoption trends enables utilities and policymakers to assess energy demand on local distribution networks, "
                "guiding upgrades to substations, feeders, and fast-charging stations. Our geographic hotspot analysis and 5-year load forecasts "
                "pinpoint where EV charging growth will stress the grid the most. Converting to a common cost-per-mile metric also helps design "
                "targeted incentives and time-of-use rates to shift charging off-peak, smoothing daily load profiles. These findings lay the "
                "groundwork for follow-on work in tariff design, renewable integration, and optimized charging strategies.",
                className="card-text"
            )
        ])

    ], style={
        "display": "grid",
        "gridTemplateColumns": "repeat(auto-fit, minmax(300px,1fr))",
        "gap": "1.5rem",
        "margin": "3rem 0"
    })
])
