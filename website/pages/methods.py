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
                    html.Div(className="method-icon-card", children=[
                        html.Img(src="https://storage.googleapis.com/evenergy163.appspot.com/icons/time.png", className="method-icon"),
                        html.H3("Time Series", className="method-title"),
                        html.P(
                            "Grouping charging sessions and energy usage by month to analyze trends.",
                            className="method-text"
                        )
                    ]),
                    html.Div(className="method-icon-card", children=[
                        html.Img(src="https://storage.googleapis.com/evenergy163.appspot.com/icons/chart.png", className="method-icon"),
                        html.H3("Line Plots", className="method-title"),
                        html.P(
                            "Displaying growth of sessions and energy delivered over time.",
                            className="method-text"
                        )
                    ]),
                    html.Div(className="method-icon-card", children=[
                        html.Img(src="https://storage.googleapis.com/evenergy163.appspot.com/icons/heatmap.png", className="method-icon"),
                        html.H3("Heatmaps", className="method-title"),
                        html.P(
                            "Visualizing charging activity by area and month in the Pacific Region.",
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
                    html.Div(className="method-icon-card", children=[
                        html.Img(src="https://storage.googleapis.com/evenergy163.appspot.com/icons/statistics_2672346.png", className="method-icon"),
                        html.H3("Descriptive Stats", className="method-title"),
                        html.P(
                            "Comparing mean and median values to assess data skew and behaviors.",
                            className="method-text"
                        )
                    ]),
                    html.Div(className="method-icon-card", children=[
                        html.Img(src="https://storage.googleapis.com/evenergy163.appspot.com/icons/cost-analysis_17994218.png", className="method-icon"),
                        html.H3("Cost Analysis", className="method-title"),
                        html.P(
                            "Comparing EV charging cost per mile vs gasoline cost.",
                            className="method-text"
                        )
                    ]),
                    html.Div(className="method-icon-card", children=[
                        html.Img(src="https://storage.googleapis.com/evenergy163.appspot.com/icons/GIS_Analysis2.jpg", className="method-icon"),
                        html.H3("Geo Analysis", className="method-title"),
                        html.P(
                            "Analyzing data geographically to understand regional usage patterns.",
                            className="method-text"
                        )
                    ]),
                ]
            ),

        ])  # end content-panel
    ]
)
