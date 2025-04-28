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
            src="", # https://storage.googleapis.com/evenergy163.appspot.com/video/Complete%20Video.mp4
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

        html.Div(
    className="card-panel",
    style={'backgroundColor': '#e0e0e0'},
    children=[
        html.H2("Broader Impacts", className="card-title"),

        # Use a bullet list to make each impact stand out
                html.Ul(
                    className="card-text",
                    style={'marginLeft': '0', 'marginRight': '20px', 'paddingLeft': '1.2em'},
                    children=[
                        html.Li([
                            html.Strong("Grid & Infrastructure Planning:"), 
                            " By mapping EV charging growth and producing 5-year load forecasts, utilities can pinpoint which regions and seasons will see the biggest spikes in electricity demand. That lets them schedule substation upgrades, reinforce distribution feeders, or deploy smart‐charging programs before localized outages or voltage issues emerge."
                        ]),
                        html.Li([
                            html.Strong("Targeted Policy & Incentives:"), 
                            " Our cost-per-mile analysis shows EVs are already cheaper to run than gasoline in most months. Policymakers can use that insight to shift subsidies away from blanket purchase rebates toward targeted programs—like workplace charging credits in areas where economic advantage alone hasn’t driven high uptake."
                        ]),
                        html.Li([
                            html.Strong("Dynamic Rate Design:"), 
                            " The short-term volatility study demonstrates that electric rates fluctuate differently from gas prices. Regulators and utilities can design time-of-use or demand-charge structures that encourage off-peak EV charging, flattening daily load profiles and lowering wholesale market risks."
                        ]),
                        html.Li([
                            html.Strong("Environmental Equity:"), 
                            " Geographic “hot spot” maps of EV adoption highlight neighborhoods where air-quality benefits from tail-pipe reduction will be greatest and where they may still lag behind. That helps environmental agencies prioritize outreach and charging infrastructure in underserved communities, ensuring the health gains of electrification reach everyone."
                        ]),
                    ]
                )
            ]
        ),

    ])
])
