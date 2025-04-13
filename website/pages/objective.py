from app import np, go, dash, dcc, html

dash.register_page(__name__, path="/objective") 

layout = html.Div([
    html.H2("Project Objective"),
    html.H3("There is 3 goals for this project: "),
    html.P("1. To analyze and visualize the Growth of EVs through trends in EV energy consumption over the years."),
    html.P("2. To examinne wheter the cost of charging an EV is cheaper than the cost of gasoline."),
    html.P("3. To provide insights or predict future energy consumption from EV."),
    html.H3("The project will use the following data sources:"),
    html.P("1. EVWatts Public Database 2019-2022"),
    html.P("2. EIA-861 Annual and Monthly Electric Power Industry Report"),
    html.P("3. EIA-923 Power Plant Operations Report 1990-2023"),
    html.P("4. Gas dataset 1"),
    html.P("5. Gas dataset 2"),
    html.P("6. Gas dataset 3"),
])
