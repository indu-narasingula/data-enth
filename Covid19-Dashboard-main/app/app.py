# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 12:14:09 2022

@author: johan
"""


import dash
from dash import dcc, html, Input, Output
import dash_labs as dl
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
#from dash_bootstrap_templates import ThemeSwitchAIO
import pandas as pd
from datetime import datetime
import time
import numpy as np
from sqlalchemy import create_engine
import os


load_figure_template("lux")

url_theme1 = dbc.themes.LUX

app = dash.Dash(__name__, plugins=[
                dl.plugins.pages], external_stylesheets=[url_theme1])
server = app.server


def last_date_per_column(df):

    columns_dict = {'besmettingen': 'Total_reported', 'ziekenhuis': 'Hospital_admission',
                    'ic': 'IC_admission', 'overleden': 'Deceased'}
    index_dict = {}

    for key in columns_dict.keys():
        search = 1
        index = -1
        while search:
            if np.isnan(df[columns_dict[key]].iat[index]):
                index += -1
            else:
                index_dict[key] = index
                search = 0

    return index_dict


DB_URL = os.environ.get('DATABASE_URL')
DB_URL = DB_URL.replace('postgres', 'postgresql')
# DB_URL =


def load_data(DB_URL):
    #con = psycopg2.connect(DB_URL)
    #cur = con.cursor()
    engine = create_engine(DB_URL, echo=False)
    query = """select * from final_df"""
    df = pd.read_sql(query, engine)
    engine.dispose()
    return df


#filepath = './files/final_df.csv'
#df_data = pd.read_csv(filepath, sep=',')

df_data = load_data(DB_URL)

last_date_dict = last_date_per_column(df_data)
time_since_update = time.time()

columns_dict = {'besmettingen': 'Total_reported', 'ziekenhuis': 'Hospital_admission',
                'ic': 'IC_admission', 'overleden': 'Deceased'}


def Card_generator(column, data, date_dict):
    # Generate the cards in the navigation bar on the left side

    card_dict = {'besmettingen': 'Besmettingen', 'ziekenhuis': 'Ziekenhuis Opnames',
                 'ic': 'IC Opnames', 'overleden': 'Overleden'}
    data_dict = {'besmettingen': 'Total_reported', 'ziekenhuis': 'Hospital_admission',
                 'ic': 'IC_admission', 'overleden': 'Deceased'}

    index = date_dict[column]
    aantal = data[data_dict[column]].iat[index]
    date = data.Date_of_statistics.iat[index]
    date = datetime.strptime(date, "%Y-%m-%d")
    date = date.strftime('%d-%m-%Y')

    card_content = [
        dbc.CardHeader(card_dict[column], className="card-header"),
        dbc.CardBody(
            [
                html.H5(aantal, className="card-title"),
                html.P(
                    date,
                    className="card-text",
                ),
            ]
        ),
    ]
    return card_content


# Create contact icons in the header top right
contact = dbc.Row(
    [
        dbc.Col(html.A(
            html.Img(src='assets/images/linkedin.png', className='img'),
            href='https://www.linkedin.com/in/johan-bekker-3501a6168/'
        )),
        # dbc.Col(html.A(
        #    html.Img(src='/assets/images/twitter.png',className='img'),
        #    href=''
        #    )),
        # dbc.Col(html.A(
        #    html.Img(src='/assets/images/kaggle.png',className='img'),
        #    href=''
        #    )),
        dbc.Col(html.A(
            html.Img(src='/assets/images/github.png', className='img',
                     id='github'),
            href='https://github.com/JohanBekker'
        )),
        # dbc.Col(
        #    dbc.Button(
        #        "Portfolio", color="link", className="ms-2", n_clicks=0,
        #        href='https://www.datascienceportfol.io/JohanBekker'
        #    ),
        #    width="auto",
        # ),

    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

# Navigation bar header
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        #dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand(
                            "Covid19 Dashboard Nederland")),
                    ],
                    align="center",
                    className="g-0",
                ),
                # href="https://plotly.com", #It's possible to make the header title a link
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                contact,  # add contact icons to header
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ], fluid=True
    ),
    color="dark",
    dark=True,
)

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    # "position": "fixed",
    # "position": "left",
    # "top": "5rem",
    "height": "150vh",
    "left": 0,
    "bottom": 0,
    # "width": "14rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    # "border": "#2C3E50",
    # "outline": "#2C3E50",
}

# Put the links to the pages in a list to use in the navigation sidebar
pages = [page for page in dash.page_registry.values()]

# Put together the sidebar components
sidebar = html.Div(
    [
        #html.H2("Sidebar", className="display-4"),
        # html.Hr(),
        dbc.Nav(
            [dbc.NavLink("Covid Cijfers", href=pages[0]["path"], active="exact"),
                dbc.NavLink("Vaccinatie Cijfers",
                            href=pages[2]["path"], active="exact"),
                dbc.NavLink("Databronnen",
                            href=pages[1]["path"], active="exact"),

                html.Br(),

                # html.P(
                #    "Laatste data:", className="text-center"
                # ),

                dbc.Card(Card_generator('besmettingen', df_data, last_date_dict),
                         color="success", inverse=True, id="besmettingen-card"),
                html.Hr(),
                dbc.Card(Card_generator('ziekenhuis', df_data, last_date_dict),
                         color="info", inverse=True, id="ziekenhuis-card"),
                html.Hr(),
                dbc.Card(Card_generator('ic', df_data, last_date_dict),
                         color="warning", inverse=True, id="ic-card"),
                html.Hr(),
                dbc.Card(Card_generator('overleden', df_data, last_date_dict),
                         color="danger", inverse=True, id="overleden-card"),
             ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE
)

# Put all components together in the layout (header, sidebar, page)
app.layout = dbc.Container([
    dbc.Row(navbar),
    dbc.Row(
        [
            dbc.Col(sidebar, width=2, style={"padding": "0rem"}),
            dbc.Col(dl.plugins.page_container, width={
                'size': 10,  "offset": 0},  className="g-0"),
        ]),
    dcc.Interval(id='interval1', interval=3600 * 1000, n_intervals=0),
    #html.Div(id='placeholder', style={'display':'none'}),

], fluid=True)


@app.callback([Output('besmettingen-card', 'children'),
               Output('ziekenhuis-card', 'children'),
               Output('ic-card', 'children'),
               Output('overleden-card', 'children')],
              Input('interval1', 'n_intervals'))
def update_cards(n):
    print('Update Cards')
    global df_data, last_date_dict

    df_data = load_data(DB_URL)
    #df_data = pd.read_csv(filepath, sep=',')
    last_date_dict = last_date_per_column(df_data)

    content1 = Card_generator('besmettingen', df_data, last_date_dict)
    content2 = Card_generator('ziekenhuis', df_data, last_date_dict)
    content3 = Card_generator('ic', df_data, last_date_dict)
    content4 = Card_generator('overleden', df_data, last_date_dict)

    return content1, content2, content3, content4

# if __name__ == "__main__":
#    app.run_server(debug=True, host='0.0.0.0')
    # app.run_server(debug=True)
