# pages/home.py
from app import np, pd, go, dash, dcc, html, px, go, os, get_csv_from_gcs, get_xlsx_from_gcs
dash.register_page(__name__, path="/") 

BUCKET_NAME = os.environ.get("BUCKET_NAME")

try: #reading energy consumption data
    data = get_xlsx_from_gcs(BUCKET_NAME, 'data/HS861 2010-.xlsx', header=2)
    data = data[['Year', 'STATE', 'Thousand Dollars.4', 'Megawatthours.4', 'Cents/kWh.4']]
    data = data[data['STATE'] == 'CA']
    data['Megawatthours.4'] = pd.to_numeric(data['Megawatthours.4'], errors='coerce')
    consumption = data
except FileNotFoundError:
    print("Energy consumption data file not found")

try:
    data = get_xlsx_from_gcs(BUCKET_NAME, 'data/annual_generation_state.xlsx', header=1)
    data = data[(data['STATE'] == 'CA') & (data['ENERGY SOURCE'] == 'Total') & (data['YEAR'] >= 2010) & (data['TYPE OF PRODUCER'] == 'Total Electric Power Industry')]
    generation = data
except FileNotFoundError:
    print('Generation Dat file not found')

# Home page layout with a plot
layout = html.Div([
    html.H2("Welcome to the EV Impact on Energy Infrastructure"),
    html.P("The adoption of electric vehicles (EVs) plays a crucial role in the transition "
    "toward sustainable transportation. In this project, we aim to examine the EV adoption "
    "trends in the United States, focusing on growth patterns, geographic distribution, vehicle "
    "characteristics, infrastructure needs, and predictive modeling to understand future adoption "
    "trends and their impact on the energy grid. Additionally, we will also be exploring whether "
    "the cost of charging EVs is economically viable to replace gasoline-powered vehicles."),
    dcc.Graph(
        id='ev-impact-plot',
        figure={
            'data': [
                go.Scatter(
                    x=consumption['Year'],
                    y=consumption['Megawatthours.4'],
                    mode='lines',
                    name='California Energy Consumption'
                ),
                go.Scatter(
                    x=generation['YEAR'],
                    y=generation['GENERATION (Megawatthours)'],
                    mode='lines',
                    name='California Energy Generation'
                )
                
            ],
            'layout': go.Layout(
                title='California Energy Consumption',
                xaxis={'title': 'Year'},
                yaxis={'title': 'Energy (MWh)'}
            )
        }
    )
])
