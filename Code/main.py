# -*- coding: utf-8 -*-

import functions as fn
import data  
import pandas as pd
import numpy as np
import scipy.optimize as opt
from scipy.optimize import minimize

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
columnas = ['Pesos', 'Dinero destinado', 'Precio', 'Titulos', 'Capital Real destinado', 'Comision individual']

tabla_temporal = pd.DataFrame(columns=columnas, index=filas).reset_index()  
tabla_temporal.rename(columns={'index':'Ticker'}, inplace=True)
tabla_temporal.sort_values('Ticker', inplace=True)

filas1 = precios["Date"]
columnas1 = ["Valor portafolio", "Rendimiento", "Rendimiento acumulado"]
pasiva = pd.DataFrame(columns=columnas1, index=filas1).reset_index() 

final.rename(columns={0:'Ticker'}, inplace=True)

pesos_inciales = data.NAFTRAC_20210129

nuevo = pesos_inciales.merge(final,on="Ticker").sort_values('Ticker')
nuevo.drop(nuevo[nuevo['Ticker'] == 'MXN'].index, inplace=True)

peso_final = nuevo['Peso (%)']/100
tabla_temporal['Pesos'] = peso_final.values
 
capital = 1000000

cash_pasivo = (1-tabla_temporal['Pesos'].sum())*capital

disp_inv_ini = capital - cash_pasivo

tabla_temporal['Dinero destinado'] = tabla_temporal['Pesos']*disp_inv_ini

tabla_temporal['Precio'] = precios.iloc[0,1:].to_list()

tabla_temporal['Titulos'] = np.round(tabla_temporal['Dinero destinado']/tabla_temporal['Precio'],0)

tabla_temporal['Capital Real destinado'] = tabla_temporal['Precio'] * tabla_temporal['Titulos']

tabla_temporal['Comision individual'] = tabla_temporal['Titulos']*tabla_temporal['Precio']*.00125

cash_real_final_pasivo =  capital - tabla_temporal['Capital Real destinado'].sum() - tabla_temporal['Comision individual'].sum()

for i in range(len(pasiva)):  
    pasiva['Valor portafolio'][i] = sum(tabla_temporal['Titulos'] * precios.iloc[i,1:].to_list()) + cash_real_final_pasivo

pasiva['Rendimiento'][0]=0
pasiva['Rendimiento acumulado'][0]=0

for i in range(len(pasiva)-1):
    pasiva['Rendimiento'][i+1]=(pasiva['Valor portafolio'][i+1]/pasiva['Valor portafolio'][i])-1
    pasiva['Rendimiento acumulado'][i+1]=sum(pasiva['Rendimiento'].iloc[0:i+2,])

#---------------------------------------------------------------------------------------------------------------------------------------------------#

#Creación de portafolio EMV
    
annual_ret_summ = pd.DataFrame(columns=[nuevo['Ticker'].to_list()], index=['Media', 'Volatilidad'])
annual_ret_summ.loc['Media'] = fn.prices_daily(tabla_temporal['Ticker'].to_list(),'2021-01-31','2022-01-31')[0].values
annual_ret_summ.loc['Volatilidad'] = fn.prices_daily(tabla_temporal['Ticker'].to_list(),'2021-01-31','2022-01-31')[1].values

corr = fn.prices_daily(tabla_temporal['Ticker'].to_list(),'2021-01-31','2022-01-31')[2].corr()

# 1. Sigma: matriz de varianza-covarianza Sigma = S.dot(corr).dot(S)
S=np.diag(annual_ret_summ.loc['Volatilidad'].values)
Sigma = S.dot(corr).dot(S)

# 2. Eind: rendimientos esperados activos individuales
Eind=annual_ret_summ.loc['Media'].values

# Número de activos
n=len(Eind)
# Dato inicial
w0=np.ones((n,))/n
# Cotas de las variables
bnds=((0,1),)*n
# Restricciones
cons={'type':'eq','fun':lambda w:w.sum()-1}

# Portafolio de mínima varianza
minvar=minimize(fun=fn.varianza,
               x0=w0,
               args=(Sigma,),
               bounds=bnds,
               constraints=cons,
               tol=1e-10)

w_minvar=minvar.x

rf=0.0429
E_minvar=Eind.T.dot(w_minvar)
s_minvar=(w_minvar.T.dot(Sigma).dot(w_minvar))**.5
RS_minvar=(E_minvar-rf)/s_minvar

# Número de activos
n=len(Eind)
# Dato inicial
w0=np.ones((n,))/n
# Cotas de las variables
bnds=((0,1),)*n
# Restricciones
cons={'type':'eq','fun':lambda w:w.sum()-1}

# Portafolio EMV
EMV=minimize(fun=fn.menos_RS,
            x0=w0,
            args=(Eind,Sigma,rf),
            bounds=bnds,
            constraints=cons,
            tol=1e-10)

w_EMV=np.round(EMV.x,4)

ponderaciones_iniciales_Activo = pd.DataFrame(w_EMV,index=nuevo['Ticker'].to_list())
ponderaciones_iniciales_Activo.rename(columns={0:'Ticker'}, inplace=True)

#---------------------------------------------------------------------------------------------------------------------------------------------------#

