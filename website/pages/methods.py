# pages/methods.py
from dash import html
from app import dash

dash.register_page(__name__, path="/methods")

layout = html.Div(
    className="page-container methods-page",
    children=[

        # 1) Page Title & Intro
        html.H2("Analytical Methods", className="section-title"),
        html.P(
            "For this project, the following analytical methods were used:",
            className="intro-text"
        ),

        # 2) Content Panel (centered white box)
        html.Div(className="content-panel", children=[

            # 2a) Group: Data Visualization
            html.H3("Data Visualization", className="subsection-title"),
            html.Div(
                className="methods-icon-grid",
                children=[

                    # Time Series
                    html.Div(className="method-icon-card", children=[
                        html.Img(
                            src="https://storage.googleapis.com/evenergy163.appspot.com/icons/time.png",
                            className="method-icon"
                        ),
                        html.H3("Time Series", className="method-title"),
                        html.P(
                            "We grouped every charging session and kWh delivered by calendar month to reveal overall trends, "
                            "seasonality (e.g. summer peaks), and long-term shifts in EV energy demand. This aggregation lays the "
                            "foundation for all subsequent analyses and forecasting.",
                            className="method-text"
                        )
                    ]),

                    # Line Plots
                    html.Div(className="method-icon-card", children=[
                        html.Img(
                            src="https://storage.googleapis.com/evenergy163.appspot.com/icons/chart.png",
                            className="method-icon"
                        ),
                        html.H3("Line Plots", className="method-title"),
                        html.P(
                            "We used time-series line charts to trace charging sessions and total energy delivered over time. "
                            "Overlaying multiple lines (e.g. sessions vs kWh, gas cost vs EV cost) makes it easy to compare growth rates "
                            "and detect divergences.",
                            className="method-text"
                        )
                    ]),

                    # Heatmaps
                    html.Div(className="method-icon-card", children=[
                        html.Img(
                            src="https://storage.googleapis.com/evenergy163.appspot.com/icons/heatmap.png",
                            className="method-icon"
                        ),
                        html.H3("Heatmaps", className="method-title"),
                        html.P(
                            "We plotted charging activity by region and month on a calendar-style heatmap to highlight geographic “hot spots.” "
                            "This reveals which areas have the fastest adoption and where demand is most concentrated at different times of year.",
                            className="method-text"
                        )
                    ]),
                ]
            ),

            # 2b) Divider
            html.Hr(className="section-divider"),

            # 2c) Group: Quantitative Analysis
            html.H3("Quantitative Analysis", className="subsection-title"),
            html.Div(
                className="methods-icon-grid",
                children=[

                    # Descriptive Statistics
                    html.Div(className="method-icon-card", children=[
                        html.Img(
                            src="https://storage.googleapis.com/evenergy163.appspot.com/icons/statistics_2672346.png",
                            className="method-icon"
                        ),
                        html.H3("Descriptive Stats", className="method-title"),
                        html.P(
                            "We computed key summary metrics such as mean, median, standard deviation and skew for both sessions and energy usage. "
                            "These stats quantify central tendencies and dispersion, helping us understand typical user behavior and identify outliers.",
                            className="method-text"
                        )
                    ]),

                    # Cost Analysis
                    html.Div(className="method-icon-card", children=[
                        html.Img(
                            src="https://storage.googleapis.com/evenergy163.appspot.com/icons/cost-analysis_17994218.png",
                            className="method-icon"
                        ),
                        html.H3("Cost Analysis", className="method-title"),
                        # now we break it into multiple paragraphs / a list
                        html.Div([
                            html.P(
                                "We converted both energy prices into a common “cost per mile” metric:",
                                className="method-text"
                            ),
                            html.Ul([
                                html.Li([
                                    html.Strong("Gas:"), " price per gallon ÷ vehicle efficiency (MPG)"
                                ], className="method-text"),
                                html.Li([
                                    html.Strong("EV:"), " price per kWh ÷ EV efficiency (mi/kWh)"
                                ], className="method-text")
                            ], style={"paddingLeft": "1rem", "marginTop": "0"}),
                            html.P(
                                "We then plotted these per-mile costs over time and added an interactive slider so you can vary MPG or mi/kWh assumptions and watch the curves update in real time.",
                                className="method-text"
                            ),
                        ])
                    ])
                    ,


                    # Geo Analysis
                    html.Div(className="method-icon-card", children=[
                        html.Img(
                            src="https://storage.googleapis.com/evenergy163.appspot.com/icons/GIS_Analysis2.jpg",
                            className="method-icon"
                        ),
                        html.H3("Geo Analysis", className="method-title"),
                        html.P(
                            "Using geographic coordinates, we mapped session counts and kWh usage across charging stations to uncover regional adoption "
                            "patterns. This spatial analysis highlights areas where infrastructure may need expansion to meet growing EV demand.",
                            className="method-text"
                        )
                    ]),
                    
                    # Correlation Analysis
                    html.Div(className="method-icon-card", children=[
                        html.Img(src="https://storage.googleapis.com/evenergy163.appspot.com/icons/correlation.png", className="method-icon"),
                        html.H3("Correlation Analysis", className="method-title"),
                        html.P(
                                "We standardized both price series (gas $/gallon and electric $/kWh) into z-scores, then computed the Pearson correlation coefficient (r). "
                                "This tells us how closely the two series move together over time—if one goes up, does the other tend to follow? "
                                "A value near +1 means strong co-movement, providing evidence of shared economic drivers.",
                            className="method-text"
                        )
                    ]),

                    # Volatility Analysis
                    html.Div(className="method-icon-card", children=[
                        html.Img(src="https://storage.googleapis.com/evenergy163.appspot.com/icons/prediction.png", className="method-icon"),
                        html.H3("Volatility Analysis", className="method-title"),
                        html.P(
                            "We calculated each month’s percentage change for gas and electric prices and plotted both changes together. "
                            "By comparing the spread (standard deviation) and cross-correlating these percentage changes, we quantified how ‘bumpy’ each market is and "
                            "whether spikes in one coincide with spikes in the other, revealing differences in short-term price behavior.",
                            className="method-text"
                        )
                    ]),

                    # Forecasting
                    html.Div(className="method-icon-card", children=[
                        html.Img(src="https://storage.googleapis.com/evenergy163.appspot.com/icons/forecasting.png", className="method-icon"),
                        html.H3("Time-Series Forecasting", className="method-title"),
                        html.P(
                            "We used Facebook Prophet, a model designed for time-series data with strong seasonality—to forecast the next five years of prices. "
                            "Prophet automatically detects yearly patterns (peaks/troughs) and fits a trend line, giving us projected trajectories plus confidence intervals. "
                            "This helps us anticipate future cost pressures and the evolving gap between gas and electricity.",
                            className="method-text"
                        )
                    ]),


                ]
            ),

        ])  # end content-panel
    ]
)
