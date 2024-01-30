# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 16:35:44 2022

@author: johan
"""

import requests
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
import dash
from sqlalchemy import create_engine
import os

dash.register_page(__name__, path="/")


def load_data(DB_URL):
    #con = psycopg2.connect(DB_URL)
    #cur = con.cursor()
    engine = create_engine(DB_URL, echo=False)
    tables = ['final_df', 'df_ziekenhuis_ic_leeftijd',
              'gevallen_per_gemeente']
    df_list = []
    for table in tables:
        query = f"""select * from {table}"""
        df = pd.read_sql(query, engine)
        df_list.append(df)
    engine.dispose()
    return df_list


DB_URL = os.environ.get('DATABASE_URL')
DB_URL = DB_URL.replace('postgres', 'postgresql')
# DB_URL =
df_data, ic_opnames_per_leeftijd, gevallen_per_gemeente = load_data(DB_URL)
ic_opnames_leeftijd = ic_opnames_per_leeftijd.groupby(
    'Age_group').sum().reset_index()


#filepath = './files/final_df.csv'
#df_data = pd.read_csv(filepath, sep=',')

#filepath2 = './files/df_ziekenhuis_ic_leeftijd.csv'
#ic_opnames_per_leeftijd = pd.read_csv(filepath2)
# ic_opnames_leeftijd = ic_opnames_per_leeftijd.groupby(
#    'Age_group').sum().reset_index()

#filepath3 = './files/gevallen_per_gemeente.csv'
#gevallen_per_gemeente = pd.read_csv(filepath3)


geojson_url = 'https://www.webuildinternet.com/articles/2015-07-19-geojson-data-of-the-netherlands/provinces.geojson'

file = requests.get(geojson_url)
geojson_file = file.json()
file.close()
per_gemeente2 = gevallen_per_gemeente.copy()
per_gemeente2['Province'].replace(
    ['Fryslân'], 'Friesland (Fryslân)', inplace=True)

data_dict = {'besmettingen': 'Total_reported', 'ziekenhuis': 'Hospital_admission',
             'ic': 'IC_admission', 'overleden': 'Deceased'}
data_dict_cumsum = {'besmettingen': 'Total_reported_cumsum', 'ziekenhuis': 'Hospital_admission_cumsum',
                    'ic': 'IC_admission_cumsum', 'overleden': 'Deceased_cumsum'}
card_dict = {'besmettingen': 'Besmettingen', 'ziekenhuis': 'Ziekenhuis Opnames',
             'ic': 'IC Opnames', 'overleden': 'Overleden'}
title_dict = {'Total_reported': 'Besmettingen', 'Hospital_admission': 'Ziekenhuis Opnames',
              'IC_admission': 'IC Opnames', 'Deceased': 'Overleden'}
title_dict_cumsum = {'Total_reported_cumsum': 'Besmettingen', 'Hospital_admission_cumsum': 'Ziekenhuis Opnames',
                     'IC_admission_cumsum': 'IC Opnames', 'Deceased_cumsum': 'Overleden'}


def get_title(data, col='Total_reported', cumsum=False):
    if data:
        date = data['points'][0]['x']
        df = df_data[df_data['Date_of_statistics'] == date]
        curr = int(df_data[col].iat[df.index[0]])
        #curr = int(data['points'][0]['y'])
        diff = int(curr - df_data[col].iat[df.index[0]-1])
    else:
        search = 1
        index = -1
        while search:
            if np.isnan(df_data[col].iat[index]):
                index += -1
            else:
                date = df_data['Date_of_statistics'].iat[index]
                search = 0

        curr = int(df_data[col].iat[index])
        diff = int(curr - df_data[col].iat[index-1])
    perc = round(diff/curr * 100, 1)
    date = pd.to_datetime(date)
    date = date.strftime("%a %b %d %Y")
    if diff < 0:
        title_name = title_dict[col]
        return f"<b>{curr} Nieuwe {title_name},\t <span style='color:#FF0000'>{diff} ({perc}%)</span></b><br><span \
        #    style='color:#4A4A4A'>{date}</span>"
    else:
        if not cumsum:
            title_name = title_dict[col]
            return f"<b>{curr} Nieuwe {title_name},\t <span style='color:#00FF00'>+{diff} (+{perc}%)</span></b><br><span \
            #    style='color:#4A4A4A'>{date}</span>"
        else:
            title_name = title_dict_cumsum[col]
            return f"<b>{curr} Totale {title_name},\t <span style='color:#00FF00'>+{diff} (+{perc}%)</span></b><br><span \
            #    style='color:#4A4A4A'>{date}</span>"


layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader(
                    dbc.Tabs(
                        [
                            dbc.Tab(label="Besmettingen", tab_id="besmettingen",
                                    tab_style={"cursor": "pointer"},
                                    label_style={"color": "#1A1A1A"}),
                            dbc.Tab(label="Ziekenhuis", tab_id="ziekenhuis",
                                    tab_style={"cursor": "pointer"},
                                    label_style={"color": "#1A1A1A"}),
                            dbc.Tab(label="IC", tab_id="ic",
                                    tab_style={"cursor": "pointer"},
                                    label_style={"color": "#1A1A1A"}),
                            dbc.Tab(label="Overleden", tab_id="overleden",
                                    tab_style={"cursor": "pointer"},
                                    label_style={"color": "#1A1A1A"}),
                        ],
                        id="tabs",
                        active_tab="besmettingen",
                    )
                ),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(dbc.Card([dbc.CardBody(dcc.Graph(id='nederland-graph', style={'height': '100%'}, config={"responsive": True}))], className="card border-primary mb-3", style={"height": "65vh"}),
                             id="card-content", className="card-text",
                             width={'size': 6,  "offset": 0, "height": "100vh"}),
                        dbc.Col(dbc.Card([dbc.CardBody(dcc.Graph(id='nederland-graph2', style={'height': '100%'}, config={"responsive": True}))], className="card border-primary mb-3", style={"height": "65vh"}),
                                id="card-content2", className="card-text",
                                width={'size': 6,  "offset": 0, "height": "100vh"}),
                    ]),
                    dbc.Row([
                        dbc.Col(dbc.Card([dbc.CardBody(dcc.Graph(id='nederland-graph3', style={"height": "100%"}, config={"responsive": True}))], className="card border-primary mb-3", style={"height": "65vh"}),
                                id="card-content3", className="card-text",
                                width={'size': 6,  "offset": 0}),
                        dbc.Col(dbc.Card([dbc.CardBody(dcc.Graph(id='nederland-graph4', style={"height": "100%"}, config={"responsive": True}))], className="card border-primary mb-3", style={"height": "65vh"}),
                                id="card-content4", className="card-text",
                                width={'size': 6,  "offset": 0}),
                    ]),
                ]),
            ], style={"height": "150vh", "outline": "#2C3E50"}),
        dcc.Interval(id='interval2', interval=3600 * 1000, n_intervals=0),
        html.Div(id='placeholder2', style={'display': 'none'}),
    ])


@callback(Output('nederland-graph', 'figure'),
          [Input('nederland-graph', 'hoverData'),
           Input("tabs", "active_tab")])
def update_graph(hdata, tabs):
    fig1 = px.bar(df_data, x="Date_of_statistics", y=data_dict[tabs],
                  title=get_title(hdata, data_dict[tabs]),
                  labels={"Total_reported": "Totaal", "Date_of_statistics": "Datum"})  # , template="simple_white")
    fig1.update_traces(marker_color='red',
                       hoverinfo='skip', hovertemplate=None)
    fig1.add_trace(go.Scatter(x=df_data["Date_of_statistics"],
                              y=df_data[data_dict[tabs]].rolling(
                                  window=7).mean().round(decimals=1),
                              mode="lines", name="Weekgemiddelde"))
    fig1.update_layout(showlegend=False, yaxis_title=None, xaxis_title=None, hovermode="x",
                       uirevision=tabs, margin=dict(b=25))
    fig1.update_yaxes(rangemode="nonnegative")
    return fig1


@callback(Output('nederland-graph2', 'figure'),
          [Input('nederland-graph2', 'hoverData'),
           Input("tabs", "active_tab")])
def update_graph2(hdata2, tabs):
    fig2 = px.line(df_data, x="Date_of_statistics", y=(data_dict_cumsum[tabs]),
                   title=get_title(hdata2, data_dict_cumsum[tabs], True),
                   hover_data={data_dict_cumsum[tabs]: False, 'Date_of_statistics': False})  # , template="simple_white")
    fig2.update_traces(line_color='red')
    fig2.update_layout(showlegend=False, yaxis_title=None,
                       xaxis_title=None, hovermode='x')
    fig2.update_yaxes(rangemode="nonnegative")
    fig2.update_layout(uirevision=tabs)
    fig2.update_layout(margin=dict(b=25))
    return fig2


@callback(Output('nederland-graph3', 'figure'),
          [Input('nederland-graph3', 'hoverData'),
           Input("tabs", "active_tab")])
def update_graph3(hdata3, tabs):
    if tabs == 'ziekenhuis' or tabs == 'ic':
        fig3 = px.pie(ic_opnames_leeftijd, values=data_dict[tabs], names='Age_group',
                      title='Totaal {} per Leeftijdsgroep'.format(
                          card_dict[tabs]),
                      labels={"Age_group": "Leeftijdsgroep", "IC_admission": "Opgenomen"})
        fig3.update_layout(uirevision=tabs)
    else:
        fig3 = px.pie(gevallen_per_gemeente, values=data_dict[tabs], names='Province',
                      title='Totale {} per Provincie'.format(card_dict[tabs]),
                      labels={"Age_group": "Leeftijdsgroep", "IC_admission": "Opgenomen"})
        fig3.update_layout(uirevision=tabs)
    return fig3


@callback(Output('nederland-graph4', 'figure'),
          [Input('nederland-graph4', 'hoverData'),
           Input("tabs", "active_tab")])
def update_graph4(hdata4, tabs):
    if tabs == 'ziekenhuis' or tabs == 'ic':
        fig4 = px.line(ic_opnames_per_leeftijd, x="Date_of_statistics_week_start",
                       y=data_dict[tabs], color='Age_group',
                       title='{} per Leeftijdsgroep'.format(card_dict[tabs]),
                       labels={"Age_group": "Leeftijdsgroep", "IC_admission": "Opgenomen",
                               "Date_of_statistics_week_start": "Datum"})
        fig4.update_yaxes(rangemode="nonnegative")
        fig4.update_layout(uirevision=tabs)
        # , hovermode='x')
        fig4.update_layout(yaxis_title=None, xaxis_title=None)
    else:
        fig4 = px.choropleth(per_gemeente2, geojson=geojson_file, locations='Province', color=data_dict[tabs],
                             featureidkey="properties.name", color_continuous_scale='reds',
                             labels={"Deceased": "Overleden", "Province": "Provincie",
                                     "Total_reported": "Besmettingen"},
                             title='Aantal {} per Provincie'.format(card_dict[tabs]))
        fig4.update_geos(fitbounds="locations", visible=False)
    return fig4


@callback(Output('placeholder2', 'children'),
          Input('interval2', 'n_intervals'))
def update_cards(n):
    global df_data, ic_opnames_per_leeftijd, ic_opnames_leeftijd
    global gevallen_per_gemeente, per_gemeente2

    print('reloading data')

    df_data, ic_opnames_per_leeftijd, gevallen_per_gemeente = load_data(DB_URL)
    ic_opnames_leeftijd = ic_opnames_per_leeftijd.groupby(
        'Age_group').sum().reset_index()

    #df_data = pd.read_csv(filepath, sep=',')

    #ic_opnames_per_leeftijd = pd.read_csv(filepath2)
    # ic_opnames_leeftijd = ic_opnames_per_leeftijd.groupby(
    #    'Age_group').sum().reset_index()

    #gevallen_per_gemeente_per_dag = pd.read_csv(filepath3)
    # gevallen_per_gemeente = gevallen_per_gemeente_per_dag.groupby(
    #    'Province').sum().reset_index()
    # per_gemeente_grouped = gevallen_per_gemeente_per_dag.groupby(
    #    ['Date_of_publication', 'Province']).sum().reset_index()

    per_gemeente2 = gevallen_per_gemeente.copy()
    per_gemeente2['Province'].replace(
        ['Fryslân'], 'Friesland (Fryslân)', inplace=True)

    return {}
