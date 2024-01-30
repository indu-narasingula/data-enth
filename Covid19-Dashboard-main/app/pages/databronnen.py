# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 16:47:49 2022

@author: johan
"""


import dash_bootstrap_components as dbc
from dash import dcc, html
import dash

dash.register_page(__name__)


layout = html.Div(
    [
        # dbc.Col(
        dbc.Card(
            [
                dbc.CardBody([
                    dcc.Markdown(
                        f"""
            -----
            ####  Data vekregen van het RIVM
            -----
            
            Alle visualisaties zijn gecreëerd met data afkomstig van het [RIVM](https://data.rivm.nl/covid-19/). De beschikbare data wordt dagelijks geupdate op de RIVM website. Vandaar dat ook de data gebruikt in de visualisaties in dit dashboard dagelijks wordt ververst zodat altijd de nieuwste data wordt gebruikt.

            Van de beschikbare datasets zijn de volgende gebruikt ter visualisatie:
            
            [COVID-19_aantallen_gemeente_per_dag.csv](https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_per_dag.csv) \n
            [COVID-19_ic_opnames.csv](https://data.rivm.nl/covid-19/COVID-19_ic_opnames.csv) \n
            [COVID-19_ziekenhuis_ic_opnames_per_leeftijdsgroep.csv](https://data.rivm.nl/covid-19/COVID-19_ziekenhuis_ic_opnames_per_leeftijdsgroep.csv) \n
            [COVID-19_ziekenhuisopnames.csv](https://data.rivm.nl/covid-19/COVID-19_ziekenhuisopnames.csv) \n
            [COVID-19_vaccinatiegraad_per_gemeente_per_week_leeftijd.csv](https://data.rivm.nl/covid-19/COVID-19_vaccinatiegraad_per_gemeente_per_week_leeftijd.csv)
            
            &nbsp;

            """
                    ),
                    html.Br(),

                    dcc.Markdown(
                        f"""
                        -----
                        #### Disclaimer
                        -----
                        
                        Dit dashboard is gecreëerd als privé project en is op geen manier gelieerd aan de Nederlandse overheid of het RIVM. De visualisaties mogen gebruikt worden op eigen risico. Er kunnen geen rechten worden ontleend aan de juistheid van de visualisaties en de data.


                        """

                    ),

                ])

            ], style={"height": "150vh", "outline": "#2C3E50"},
        )
    ])
