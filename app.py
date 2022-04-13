import os

import plotly.express as px
import pandas as pd
import numpy as np
from dash import Dash
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html

transformed = pd.read_csv("data/transformed.csv")
transformed = transformed.loc[transformed['Year'] > 1994, :]

n_colors = len(transformed.Country.unique())
colorscale = colors = px.colors.sample_colorscale("viridis" ,[n/(n_colors -1) for n in range(n_colors)])
colordict = {f:colorscale[i] for i, f in enumerate(transformed.Country.unique())}


quick_dictionary = dict()
quick_dictionary['Internet'] = '% de habitantes usando Internet'
quick_dictionary['Móvil'] = 'Número de moviles para 100 habitantes'
quick_dictionary['Banda Ancha'] = '% de empresas usando el internet de la velocidad alta'


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.title = "Creativo_piasecki"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="El desarollo de varios medios de telecomunicacíon", className="header-title"
                ),
                html.P(
                    children="Este app muestra desarrollo de diferentes aspectos de telecomunicacíon en varios paises. Todos"
                             " datos son cogidos de World Bank Open Data. Adémas el grafo de GDP deja comparar el desarrollo de telecomunicacíón "
                             "y el desarollamiento de economía",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="País", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": country, "value": country}
                                for country in np.sort(transformed.Country.unique())
                            ],
                            value="Spain",
                            clearable=False,
                            className="dropdown",
                            multi=True
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Tipo de telecomunicacíón", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {"label": telecomunnicacion_type, "value": telecomunnicacion_type}
                                for telecomunnicacion_type in ["Móvil", "Internet", "Banda Ancha"]
                            ],
                            value="Internet",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    [
        Output("price-chart", "figure"),
        Output("volume-chart", "figure")
    ],
    [
        Input("region-filter", "value"),
        Input("type-filter", "value"),
        #Input("date-range", "year"),
        #Input("date-range", "end_date"),
    ],
)



def update_charts(country, telecommunication_type):

    if type(country) == str:
        mask = (
            (transformed['Country'] == country)
        )
    else:
        mask = (
            (transformed['Country'].isin(country))
        )

    filtered_data = transformed.loc[mask, :]

    price_chart_figure = px.line(
        filtered_data,
        x = 'Year',
        y=telecommunication_type,
        color='Country',
        color_discrete_map=colordict,
        title=quick_dictionary[telecommunication_type],
        markers=True
    )
    price_chart_figure.update_layout(
        {'paper_bgcolor': 'rgba(0,0,0,0)',
         'plot_bgcolor': 'rgba(0,0,0,0)'},
    )
    volume_chart_figure = px.line(
        filtered_data,
        x='Year',
        y='GDP per capita',
        color='Country',
        color_discrete_map=colordict,
        title="GDP Per Capita",
        markers=True
    )
    volume_chart_figure.update_layout(
        {'paper_bgcolor': 'rgba(0,0,0,0)',
         'plot_bgcolor': 'rgba(0,0,0,0)'},
    )

    return price_chart_figure, volume_chart_figure
if __name__ == "__main__":
    app.run_server(debug=True)
