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
                            "We took the count of charging sessions and grouped energy (kWh) delivered by calendar month to reveal overall trends, "
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
                            "We filtered the data to the pacific region, and then used a line plot to find the most popular locations. "
                            "Next, we use heatmap to visualize the growth of the top locations over time. This is just another way to visualize "
                            "growth in popular areas.",
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
                            "Using the regions column on the dataset, we did a charging session count and aggregation for energy (kWh) usage on the pacific region to uncover EV growth "
                            "patterns. This spatial analysis highlights metro areas monthly growth rates, and where infrastructure may need expansion to meet growing EV demand.",
                            className="method-text"
                        )
                    ]),
                    
                    # Correlation Analysis
                    html.Div(className="method-icon-card", children=[
                        html.Img(src="https://storage.googleapis.com/evenergy163.appspot.com/icons/correlation.png", className="method-icon"),
                        html.H3("Correlation Analysis", className="method-title"),
                        html.P(
                                "We standardized both price series (gas $/gallon and electric $/kWh) into z-scores, then computed the Pearson correlation coefficient (r). "
                                "This tells us how closely the two series move together over time whether if one goes up, does the other tend to follow? "
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
                    #Linear Growth Rate
                    html.Div(className="method-icon-card", children=[
                        html.Img(src="https://storage.googleapis.com/evenergy163.appspot.com/icons/spectrum_2938677.png", className="method-icon"),
                        html.H3("Linear Growth Rate", className="method-title"),
                        html.P(
                            "We calculated the monthly growth rate for linear trends by using the formula: linear-coeff or slope * 30 days, "
                            "divide by the mean of the y values. Then multiply by 100 to get the percentage for average monthly growth rate. ",
                            className="method-text"
                        )
                    ]),

                    # Exponential Growth Rate
                    html.Div(className="method-icon-card", children=[
                        html.Img(src="https://storage.googleapis.com/evenergy163.appspot.com/icons/business_13867188.png", className="method-icon"),
                        html.H3("Exponential Growth Rate", className="method-title"),
                        html.P(
                            "We calculated the exponential monthly growth rate by using the formula: (exp(coef) - 1) * 100, "
                            "where coef is the coefficient of the exponential trend line. This gives us the average monthly growth rate as a percentage.",
                            className="method-text"
                        )
                    ]),

                    # Linear Regression Model
                    html.Div(className="method-icon-card", children=[
                        html.Img(src="https://storage.googleapis.com/evenergy163.appspot.com/icons/correlation.png", className="method-icon"),
                        html.H3("Linear Regression", className="method-title"),
                        html.P(
                                "We used Linear regression model to determine where a trend is either linear or exponential. For exponential model, "
                                "we fitted the model with the log transformed y values. Transform exponenetial data to linear data. Then we compared both models "
                                "r-squared values to determine which model fits better. ",
                            className="method-text"
                        )
                    ]),


                ]
            ),

        ])  # end content-panel
    ]
)
