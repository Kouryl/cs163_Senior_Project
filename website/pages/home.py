# pages/home.py
import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div(className="page-container", children=[

    html.H1(
        "EV Growth and Its Effect on Energy Demand",
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
    
html.Div(
    className="video-caption",
    children=[
        "Video courtesy of ",
        html.A(
            "YouTube – Autel MaxiChargers | EV Charging Stations",
            href="https://www.youtube.com/watch?v=juoAoIqexJs",
            target="_blank",
            rel="noopener noreferrer"
        ),
        " (Nov 18, 2021)"
    ]
),

    html.Div(className="cards-container", children=[

        # Project Overview
        html.Div(className="card-panel", children=[
            html.H2("Project Overview", className="card-title"),
            html.Div(
                    "We analyzed monthly EV charging sessions and energy delivered across Pacific-region metros "
                    "to uncover growth trends and seasonal cycles. Historical gasoline and electricity rates were "
                    "converted into a common cost-per-mile metric to compare operating costs, and we examined both "
                    "their short-term volatility and long-term co-movement. We then used 39 months of historical "
                    "energy data to forecast next year’s Pacific-region electricity demand using Facebook Prophet, "
                    "which handles non-stationary seasonal patterns.",
                className="card-text"
            )
        ]),

        # Broader Impacts
        html.Div(className="card-panel", children=[
            html.H2("Broader Impacts", className="card-title"),
            html.Div(
                "Understanding EV adoption trends enables utilities and policymakers to assess energy demand on local distribution networks, "
                "guiding upgrades to substations, feeders, and fast-charging stations. Metro‐area growth maps reveal which Pacific-region corridors will "
                "experience the fastest EV uptake, guiding strategic placement of new fast-charging stations. Five-year forecasts of energy prices "
                "could allow a more accurate budget setting, hedging strategies, and investment timing.",
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
