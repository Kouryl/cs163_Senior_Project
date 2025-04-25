from dash import html
from app import dash

dash.register_page(__name__, path="/objective")

layout = html.Div(className="page-container", children=[
    html.H2("Project Objective", className="page-title"),
    html.P("This project pursues three core goals:", className="intro-text"),

    # Goals grid
    html.Div(className="objective-container", children=[
        html.Div(className="objective-card", children=[
            html.H3("1. Analyze Trends", className="card-title"),
            html.Div(
                "Analyze historical and current data to visualize trends in EV energy consumption, illustrating the growth of EV adoption over time.",
                className="card-text"
            )
        ]),
        html.Div(className="objective-card", children=[
            html.H3("2. Evaluate Cost Advantage", className="card-title"),
            html.Div(
                "Determine whether the cost of charging an EV provides a financial advantage over gasoline by examining electricity rates, gas prices, and overall cost per mile.",
                className="card-text"
            )
        ]),
        html.Div(className="objective-card", children=[
            html.H3("3. Forecast Future Demand", className="card-title"),
            html.Div(
                "Provide insights into potential future energy consumption by EVs, including forecasts that help stakeholders understand and prepare for shifts in demand.",
                className="card-text"
            )
        ]),
    ]),

    html.Hr(className="section-divider"),

    html.H3("Data Sources", className="section-title"),
    # Sources grid
    html.Div(className="objective-container", children=[
        html.Div(className="objective-card", children=[
            html.H4("EVWatts Public Database (2019–2022)", className="card-title"),
            html.Div([
                html.A("Visit Source", href="https://www.clearesult.com/insights/evwatts", target="_blank", className="source-link")
            ], className="card-text")
        ]),
        html.Div(className="objective-card", children=[
            html.H4("IEA Global EV Data Explorer", className="card-title"),
            html.Div([
                html.A("Visit Source", href="https://www.iea.org/data-and-statistics/data-tools/global-ev-data-explorer", target="_blank", className="source-link")
            ], className="card-text")
        ]),
        html.Div(className="objective-card", children=[
            html.H4("EIA Gasoline Prices", className="card-title"),
            html.Div([
                html.A("Visit Source", href="https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=pet&s=emm_epm0_pte_sca_dpg&f=m", target="_blank", className="source-link")
            ], className="card-text")
        ]),
        html.Div(className="objective-card", children=[
            html.H4("California Electricity Rates", className="card-title"),
            html.Div([
                html.A("Visit Source", href="https://ycharts.com/indicators/california_electric_utility_retail_price", target="_blank", className="source-link")
            ], className="card-text")
        ]),
    ]),
])
