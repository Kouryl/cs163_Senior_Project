# pages/predictions.py
from dash import html
from app import dash

dash.register_page(__name__, path="/predictions")

layout = html.Div(className="page-container predictions-page", children=[

    # 1) Page title
    html.H2("Future Electric Predictions", className="section-title",style={"color": "#000000"}),

    # 2) Intro paragraph
    html.Div(className="predictions-intro", children=[
        html.P(
            "The dataset had a total of 39 months, which means that we can do a forecasting of "
            "energy usage for the next year. The data also had a p-value of 0.993, which means the "
            "data is not stationary. For this forecasting, we also used Meta's Prophet, which handles "
            "non-stationary data.",
            className="content-text"
        )
    ]),

    # 3) Chart + Info + Summary in a responsive grid
    html.Div(className="predictions-grid", children=[

        # 3a) Left column: chart + info line
        html.Div(className="predictions-chart-block", children=[
            html.Img(
                src="https://storage.googleapis.com/evenergy163.appspot.com/new_results/pacific_results/pacific_prediction_energy.png",
                className="prediction-image"
            ),
            html.P(
                "(Info: Forecast of energy usage for the Pacific region.)",
                className="info-text"
            )
        ]),

        # 3b) Right column: chart summary
        html.Div(className="predictions-summary-block", children=[
            html.P(
                "Summary: This plot shows the future electric predictions for the Pacific region. "
                "The yellow dotted line represents the predicted energy usage, while the blue line "
                "represents the actual energy usage from the past. Here we can see that the model is "
                "predicting an upward trend.",
                className="content-text"
            )
        ])
    ]),

    # 4) Final summary heading
    html.H3("Summary", className="subsection-title"),

    # 5) Final summary text
    html.Div(className="content-text", children=[
        "Though we lack the data to analyze actual impact to the energy infrastructure, our analysis "
        "of the past, and the predictions suggest strong growth in EV adoption, and energy usage. "
        "Therefore based on the data and strong evidence of consistent upward trends we can infer that "
        "the upward trend suggests a growing pressure on the infrastructure and grid, which highlights "
        "the need for proactive planning to support future EV demands."
    ])

])
