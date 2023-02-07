# -*- coding: utf-8 -*-

import functions as fn
import data 
import pandas as pd
import numpy as np
 
tickers = pd.DataFrame({'tickers':(np.concatenate((data.NAFTRAC_20210129.iloc[:, 0],
                          data.NAFTRAC_20210226.iloc[:, 0],
                          data.NAFTRAC_20210331.iloc[:, 0],
                          data.NAFTRAC_20210430.iloc[:, 0],
                          data.NAFTRAC_20210531.iloc[:, 0],
                          data.NAFTRAC_20210630.iloc[:, 0],
                          data.NAFTRAC_20210730.iloc[:, 0],
                          data.NAFTRAC_20210831.iloc[:, 0],
                          data.NAFTRAC_20210930.iloc[:, 0],
                          data.NAFTRAC_20211026.iloc[:, 0],
                          data.NAFTRAC_20211130.iloc[:, 0],
                          data.NAFTRAC_20211231.iloc[:, 0],
                          data.NAFTRAC_20220126.iloc[:, 0],
                          data.NAFTRAC_20220228.iloc[:, 0],
                          data.NAFTRAC_20220331.iloc[:, 0],
                          data.NAFTRAC_20220429.iloc[:, 0],
                          data.NAFTRAC_20220531.iloc[:, 0],
                          data.NAFTRAC_20220630.iloc[:, 0],
                          data.NAFTRAC_20220729.iloc[:, 0],
                          data.NAFTRAC_20220831.iloc[:, 0], 
                          data.NAFTRAC_20220930.iloc[:, 0],
                          data.NAFTRAC_20221031.iloc[:, 0],
                          data.NAFTRAC_20221130.iloc[:, 0],
                          data.NAFTRAC_20221230.iloc[:, 0],
                          data.NAFTRAC_20230125.iloc[:, 0],
                          ), axis=None))})

freq = tickers['tickers'].value_counts()

final = pd.DataFrame(freq[freq==25].index.tolist())

final.to_csv('../files/tickers.csv')

precios = pd.read_csv('../files/precios.csv')
precios.drop(['Unnamed: 0'], axis=1, inplace=True)

filas = data.tickers_fin1
columnas = ['Pesos', 'Dinero destinado', 'Titulos', 'Valor por accion', 'Comision individual']

tabla_temporal = pd.DataFrame(columns=columnas, index=filas).reset_index()  
tabla_temporal.rename(columns={'index':'Tickers'}, inplace=True)

filas1 = precios["Date"]
columnas1 = ["Valor portafolio", "Rendimiento", "Rendimiento acumulado"]
pasiva = pd.DataFrame(columns=columnas1, index=filas1).reset_index() 