# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 20:16:17 2022

@author: johan
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 18:11:46 2022

@author: johan
"""

#import requests
#import csv
#import time


#from pathlib import Path




from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import datetime
import os
class Dataset:

    def __init__(self):
        #self.path_besmettingen_overlijdens_per_gemeente = 'data/COVID-19_aantallen_gemeente_per_dag.csv'
        #self.path_ziekenhuis = 'data/COVID-19_ziekenhuisopnames.csv'
        #self.path_ic = 'data/COVID-19_ic_opnames.csv'

        self.url_besmettingen_overlijdens_per_gemeente = 'https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_per_dag.csv'
        self.url_ziekenhuis = 'https://data.rivm.nl/covid-19/COVID-19_ziekenhuisopnames.csv'
        self.url_ic = 'https://data.rivm.nl/covid-19/COVID-19_ic_opnames.csv'

        self.url_ziekenhuis_ic_leeftijd = 'https://data.rivm.nl/covid-19/COVID-19_ziekenhuis_ic_opnames_per_leeftijdsgroep.csv'

        self.url_vaccinatiegraad_per_wijk_per_week = 'https://data.rivm.nl/covid-19/COVID-19_vaccinatiegraad_per_gemeente_per_week_leeftijd.csv'

        #self.filepath = './final_df.csv'
        #self.filepath2 = './df_ziekenhuis_ic_leeftijd.csv'
        #self.filepath3 = './df_gemeentes_per_dag.csv'
        #self.filepath4 = './vaccinatiegraad_per_wijk_per_week.csv'

        DB_URL = os.environ.get('DATABASE_URL')
        self.DB_URL = DB_URL.replace('postgres', 'postgresql')
        # self.DB_URL =

        self.file_path = './files/'
        self.filepath = 'final_df.csv'
        self.filepath2 = 'df_ziekenhuis_ic_leeftijd.csv'
        self.filepath3 = 'gevallen_per_gemeente.csv'
        self.filepath4 = 'vaccinatiegraad_per_wijk_per_week.csv'

        #self.url_besmettingen_overlijdens_per_gemeente ='https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_per_dag.json'
        #self.url_ziekenhuis = 'https://data.rivm.nl/covid-19/COVID-19_ziekenhuisopnames.json'
        #self.url_ic = 'https://data.rivm.nl/covid-19/COVID-19_ic_opnames.json'

    def download(self):
        df1 = pd.read_csv(
            self.url_besmettingen_overlijdens_per_gemeente, sep=';')
        df2 = pd.read_csv(self.url_ziekenhuis, sep=';')
        df3 = pd.read_csv(self.url_ic, sep=';')

        df4 = pd.read_csv(self.url_ziekenhuis_ic_leeftijd, sep=';')

        df5 = pd.read_csv(self.url_vaccinatiegraad_per_wijk_per_week, sep=';')

        return df1, df2, df3, df4, df5

    def process_data(self, df1, df2, ic_opnames):
        gevallen_per_dag = df1.groupby(
            'Date_of_publication').sum().reset_index()
        ziekenhuis_opnames_dag = df2.groupby(
            'Date_of_statistics').sum().reset_index()
        gevallen_per_dag.rename(
            columns={'Date_of_publication': 'Date_of_statistics'}, inplace=True)

        full_df = ic_opnames.merge(
            gevallen_per_dag, on='Date_of_statistics', how="outer")
        full_df = full_df.merge(ziekenhuis_opnames_dag,
                                on='Date_of_statistics', how="outer")

        columns = ['Total_reported', 'Deceased',
                   'Hospital_admission', 'IC_admission']
        cumsum_columns = [column + '_cumsum' for column in columns]

        full_df[cumsum_columns] = full_df[columns].cumsum()

        full_df[['Total_reported', 'Deceased', 'Hospital_admission']]

        return full_df[['Date_of_statistics', 'IC_admission', 'Total_reported', 'Deceased',
                        'Hospital_admission', 'IC_admission_cumsum', 'Total_reported_cumsum',
                        'Deceased_cumsum', 'Hospital_admission_cumsum']]

    def update(self):
        print('Update is called')
        # Update the data every hour
        # if time.time() - self.time > 3600 or self.startup == True:

        df_besmettingen, df_ziekenhuis, df_ic, df_ziekenhuis_ic_leeftijd, df5 = self.download()
        final_df = self.process_data(
            df_besmettingen.copy(), df_ziekenhuis, df_ic)
        #final_df = full_df[['Date_of_statistics', 'IC_admission', 'Total_reported', 'Deceased', 'Hospital_admission']]

        #final_df.to_csv(self.file_path + self.filepath)

        #df_ziekenhuis_ic_leeftijd.to_csv(self.file_path + self.filepath2)

        #df_besmettingen.to_csv(self.file_path + self.filepath3)
        df_gevallen_per_gemeente = df_besmettingen.groupby(
            'Province').sum().reset_index()
        #df_gevallen_per_gemeente.to_csv(self.file_path + self.filepath3)

        df5.drop(['Version', 'Date_of_report'], axis=1, inplace=True)
        df5.sort_values(by='Region_name', inplace=True)
        #df5.to_csv(self.file_path + self.filepath4)

        engine = create_engine(self.DB_URL, echo=False)
        final_df.to_sql(self.filepath.replace('.csv', ''),
                        con=engine, if_exists='replace')
        df_ziekenhuis_ic_leeftijd.to_sql(
            self.filepath2.replace('.csv', ''), con=engine, if_exists='replace')
        df_gevallen_per_gemeente.to_sql(
            self.filepath3.replace('.csv', ''), con=engine, if_exists='replace')
        df5.to_sql(self.filepath4.replace('.csv', ''),
                   con=engine, if_exists='replace')
        engine.dispose()

        print('Update Complete')

        #path = Path(self.filepath4)
        # print(path.parent.absolute())

        # self.startup=False
        #self.time = time.time()
        #self.startup = False

# =============================================================================
#     def last_date_per_column(self, df):
#
#         columns_dict = {'besmettingen': 'Total_reported', 'ziekenhuis': 'Hospital_admission',
#                 'ic': 'IC_admission', 'overleden': 'Deceased'}
#         index_dict = {}
#
#         for key in columns_dict.keys():
#             search = 1
#             index = -1
#             while search:
#                 if np.isnan(df[columns_dict[key]].iat[index]):
#                     index += -1
#                 else:
#                     index_dict[key] = index
#                     search = 0
#
#
#
#         return index_dict
# =============================================================================
