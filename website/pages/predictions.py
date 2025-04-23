from app import np, go, dash, dcc, html

dash.register_page(__name__, path="/predictions") 
layout = html.Div([
    html.H2("Future Electric Predictions"),
    html.P("The dataset had a total of 39 months, which means that we can do a forecasting of "
           "energy usage for the next year. The data also had a p-value of 0.993, which means the "
           "data is not stationary. For this forecasting, we also used Meta's Prohpet, which handles "
           "non-stationary data.",
           style={'max-width': '50vw'}),

    html.Img(src="https://storage.googleapis.com/evenergy163.appspot.com/new_results/pacific_results/pacific_prediction_energy.png",
             style={"width": '50%', "height": "auto",  "margin": 'auto 50px' }),
    html.P("Summary: This plot shows the future electric predictions for the Pacific region. "
           "The yellow dotted line represents the predicted energy usage, while the blue line "
           "represents the actual energy usage from the past. Here we can see that the model is "
           "predicting an upward trend.", 
           style={'max-width': '50vw'}),
    
    html.H3("Summary:"),
    html.P("Though we lack the data to analyze actual impact to the energy infrastructure, our analysis "
           "of the past, and the predictions suggest strong growth in EV adoption, and energy usage. "
           "Therefore based on the data and strong evidence of consistent upward trends "
           "we can infer that the upward trend suggest a growing pressure on the infrastructure and grid, "
           "which highlights the need for proactive planning to support future EV demands.",
           style={'max-width': '50vw'})

])
