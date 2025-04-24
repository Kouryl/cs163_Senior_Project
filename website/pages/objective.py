from app import np, go, dash, dcc, html

dash.register_page(__name__, path="/objective") 

layout = html.Div([
    html.H2("Project Objective"),
    html.H3("There are 3 goals for this project: "),
    html.P("1. Analyze historical and current data to visualize trends in EV energy consumption, illustrating the growth of EV adoption over time."),
    html.P("2. Determine whether the cost of charging an EV provides a financial advantage over gasoline by examining electricity rates, gas prices, and overall cost per mile."),
    html.P("3. Provide insights into potential future energy consumption by EVs, including forecasts that help stakeholders understand and prepare for shifts in demand."),
    html.H3("The project will use the following data sources:"),
    html.P("1. EVWatts Public Database 2019-2022"),
    html.P("2. EIA-861 Annual and Monthly Electric Power Industry Report"),
    html.P("3. EIA-923 Power Plant Operations Report 1990-2023"),
    html.P([
        "4. ",
        html.A(
            "California All Grades All Formulations Retail Gasoline Prices (Dollars per Gallon)", 
            href="https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=pet&s=emm_epm0_pte_sca_dpg&f=m", 
            target="_blank",
            style={'color': '#0000EE', 'textDecoration': 'underline'}
        )
    ]),
    html.P([
        "5. ",
        html.A(
            "California Electric Utility Retail Price (USD/kWh)", 
            href="https://ycharts.com/indicators/california_electric_utility_retail_price", 
            target="_blank",
            style={'color': '#0000EE', 'textDecoration': 'underline'}
        )
    ])
])
