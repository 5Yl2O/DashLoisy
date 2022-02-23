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

#print(df_eau.columns)
#print(set(df_eau.code_parametre))

# ------------------------------------------------------------------------------
page_title=html.Div(html.H1("Qualité sanitaire de l'eau des sources de Loisy"))

dd_menu=dcc.Dropdown(id="select_param",
                 options=[
                     {"label": 'Nitrates (en NO3)', "value": '1340'},
                     {"label": "Conductivité à 25°C", "value": '1303'},
                     {"label": "Chlore combiné", "value": '1755'},
                     {"label": "Chlore total", "value": '1399'}
                 ],
                 value='1340',
                 )
# App layout
app.layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                page_title,
                md=11,
            ),

        ),
        dbc.Row(
            dbc.Col(
                [
                    dd_menu,
                    html.Div(id='output_container', children=[]),
                    dcc.Graph(id='my_conc', figure={}),
                ],
                md=11,
            ),
            justify='center'
        ),

        dbc.Row(
            dbc.Col(
                dl.Map(
                    dl.TileLayer(), style={'height': '50vh'}
                ),
                md=11,
            ),
        justify="center",
        ),
        dbc.Row(
            [
                html.Br(),
                html.Div('Réalisé par XX Votre nom ici !! XX'),
                html.Br(),
            ],
            justify='center'
        ),

    ],
    className="pad-row"
    )


# ------------------------------------------------------------------------------

# Connection du graph Plotly avec les composants Dash (dcc)
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_conc', component_property='figure')],
    [Input(component_id='select_param', component_property='value')]
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
