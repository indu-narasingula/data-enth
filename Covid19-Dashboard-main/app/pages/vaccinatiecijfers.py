# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 12:15:17 2022

@author: johan
"""

import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback, dash_table
import dash
from sqlalchemy import create_engine
import os

dash.register_page(__name__)

DB_URL = os.environ.get('DATABASE_URL')
DB_URL = DB_URL.replace('postgres', 'postgresql')
# DB_URL =


def load_data(DB_URL):
    #con = psycopg2.connect(DB_URL)
    #cur = con.cursor()
    engine = create_engine(DB_URL, echo=False)
    query = """select * from vaccinatiegraad_per_wijk_per_week"""
    df = pd.read_sql(query, engine)
    engine.dispose()
    return df


df = load_data(DB_URL)
df.reset_index(inplace=True, drop=True)

#filepath4 = './files/vaccinatiegraad_per_wijk_per_week.csv'
#df = pd.read_csv(filepath4)
#df.reset_index(inplace=True, drop=True)

columns = ['Date_of_statistics', 'Region_name', 'Birth_year',
           'Vaccination_coverage_partly', 'Vaccination_coverage_completed', 'Age_group']
column_dict = {'Date_of_statistics': 'Datum', 'Region_name': 'Naam', 'Birth_year': 'Geboortejaar',
               'Vaccination_coverage_partly': 'Gedeeltelijk Gevaccineerd', 'Vaccination_coverage_completed': 'Volledig Gevaccineerd', 'Age_group': 'Leeftijdsgroep'}

df_veiligheidsregio = df[df['Region_level'] ==
                         'Veiligheidsregio'].reset_index(drop=True)
df_veiligheidsregio = df_veiligheidsregio[columns]
df_gemeente = df[df['Region_level'] == 'Gemeente'].reset_index(drop=True)
df_gemeente = df_gemeente[columns]

layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader(
                    dbc.Tabs(
                        [
                            dbc.Tab(label="Gemeente", tab_id="gemeente",
                                    tab_style={"cursor": "pointer"},
                                    label_style={"color": "#1A1A1A"}),
                            dbc.Tab(label="Veiligheidsregio", tab_id="veiligheidsregio",
                                    tab_style={"cursor": "pointer"},
                                    label_style={"color": "#1A1A1A"}),
                        ],
                        id="tabs",
                        active_tab="gemeente",
                    )
                ),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(dash_table.DataTable(id='vaccination_table',
                                                     columns=[
                                                         {'id': key, 'name': column_dict[key]} for key in column_dict.keys()],
                                                     page_size=200,
                                                     style_table={
                                                         'height': '800px', 'whiteSpace': 'normal'},
                             fixed_rows={'headers': True},
                             style_cell_conditional=[{'if': {'column_id': 'Region_name'},
                                                      'width': '18%'},
                                                         {'if': {'column_id': 'Date_of_statistics'},
                                                          'width': '10%'},
                                                         {'if': {'column_id': 'Birth_year'},
                                                          'width': '11%'},
                                                         {'if': {'column_id': 'Age_group'},
                                                          'width': '14%'}],
                             style_data={'color': 'black',
                                                         'backgroundColor': 'white'},
                             style_data_conditional=[
                                                         {'if': {'row_index': 'odd'},
                                                          'backgroundColor': 'rgb(220, 220, 220)'}
                                                     ],
                             style_header={
                                                         'backgroundColor': '#343A40',
                                                         'color': 'white',
                                                         'fontWeight': 'bold'
                                                     }
                             ),
                            id="card-content", className="card-text",
                            width={'size': 12,  "offset": 0}),
                    ]),
                ])

            ], style={"height": "150vh", "outline": "#2C3E50"},
        ),
        dcc.Interval(id='interval3', interval=3600 * 1000, n_intervals=0),
        html.Div(id='placeholder3', style={'display': 'none'}),
    ]),


@callback(Output('vaccination_table', 'data'),
          Input('tabs', 'active_tab'))
def update_table(tabs):
    if tabs == "gemeente":
        return df_gemeente.to_dict('records')
    else:
        return df_veiligheidsregio.to_dict('records')


@callback(Output('placeholder3', 'children'),
          Input('interval3', 'n_intervals'))
def update_cards(n):
    global df, df_veiligheidsregio, df_gemeente
    #df = pd.read_csv(filepath4)
    #df.reset_index(inplace=True, drop=True)

    df = load_data(DB_URL)
    df.reset_index(inplace=True, drop=True)

    df_veiligheidsregio = df[df['Region_level'] ==
                             'Veiligheidsregio'].reset_index(drop=True)
    df_veiligheidsregio = df_veiligheidsregio[columns]
    df_gemeente = df[df['Region_level'] == 'Gemeente'].reset_index(drop=True)
    df_gemeente = df_gemeente[columns]
    return {}
