# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import plotly.express as px
import pandas as pd
import requests


bootstrap_theme=[dbc.themes.LITERA]
app = Dash(__name__,external_stylesheets=bootstrap_theme)

#import des données HubEaux sur les nitrates (param 1340)

# Construction de la requete html

base ='http://hubeau.eaufrance.fr/'
api ='api/vbeta/qualite_eau_potable/resultats_dis'
requete ='?code_commune=54320&nom_uge=LOISY'

url = base + api + requete

r=requests.get(url)
res = r.json()
df_eau=pd.DataFrame.from_dict(res['data'])


# ------------------------------------------------------------------------------


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
)

# App layout
app.layout = html.Div([

    html.H1("Qualité sanitaire de l'eau des sources de Loisy", style={'text-align': 'center'}),

# la liste des codes param est extraite du df_eau => df[['code_parametre','libelle_parametre']]



    
    dcc.Dropdown(id="slct_param",
                 children=[
                     {"label": 'Nitrates (en NO3)', "value": 1340},
                     {"label": "Conductivité à 25°C", "value": 1303},
                     {"label": "Chlore combiné", "value": 1755},
                     {"label": "Chlore total", "value": 1399}
                 ],
                 multi=False,
                 value='1340',
                 className='col-md-6 mb-3'
                 ),


    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_conc', figure={})

])


# ------------------------------------------------------------------------------

# Connection du graph Plotly avec les composants Dash (dcc)
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_conc', component_property='figure')],
    [Input(component_id='slct_param', component_property='value')]
)
def update_graph(option_slctd):

    container = "Le code du paramètre selectionné est: {}".format(option_slctd)

    dff = df_eau.copy()
    dff = dff[dff["code_parametre"] == option_slctd]


    # Plotly Express
    #Création du graph

    fig_eau = px.line(dff,
                      x='date_prelevement',
                      y='resultat_numerique',
                      color='nom_uge',
                      markers=True
                      )

    return container, fig_eau


if __name__ == '__main__':
    app.run_server(debug=True)
