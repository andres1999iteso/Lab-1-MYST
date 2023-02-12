# -*- coding: utf-8 -*-

import functions as fn
import data  
import pandas as pd
import numpy as np
import scipy.optimize as opt
from scipy.optimize import minimize
import yfinance as yf

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

df_pasiva = pasiva
#---------------------------------------------------------------------------------------------------------------------------------------------------#

#Creación de portafolio EMV
    
annual_ret_summ = pd.DataFrame(columns=[nuevo['Ticker'].to_list()], index=['Media', 'Volatilidad'])
annual_ret_summ.loc['Media'] = fn.prices_daily(tabla_temporal['Ticker'].to_list(),'2021-01-29','2022-01-26')[0].values
annual_ret_summ.loc['Volatilidad'] = fn.prices_daily(tabla_temporal['Ticker'].to_list(),'2021-01-29','2022-01-26')[1].values

corr = fn.prices_daily(tabla_temporal['Ticker'].to_list(),'2021-01-29','2022-01-26')[2].corr()

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

ponderaciones_iniciales_Activo_minimize = pd.DataFrame(w_EMV,index=nuevo['Ticker'].to_list())
ponderaciones_iniciales_Activo_minimize.rename(columns={0:'Ticker'}, inplace=True)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
#Ponderaciones con montecarlo

# Matriz de covarianza
Sigma=fn.prices_daily(tabla_temporal['Ticker'].to_list(),'2021-01-29','2022-01-26')[2].cov()

# Matriz de correlación
R=corr

# Definimos el número de portafolios que simularemos, y la cantidad de activos que tenemos
n_port=1000000
n_act=31

# Generar una matriz de pesos de n_portafolios x n_activos,
# tal que cada fila sume uno (recordar restricción)
np.random.seed(1)
W=np.random.dirichlet(alpha=np.ones(n_act),size=n_port)

# Rendimientos y volatilidad de cada portafolios
Eind=annual_ret_summ.loc['Media'].values
Erp=W.dot(Eind)

#Volatilidad de los 1000000 portafolios
sp=np.zeros(n_port)
for i in range (n_port):
    w=W[i,:]
    sp[i]=(w.T.dot(Sigma).dot(w))**.5 
    
# Radio de Sharpe
RS = (Erp - rf)/sp

# Data frame de resultados
portafolios=pd.DataFrame(data={tabla_temporal['Ticker'][16]:W[:,0],
                               tabla_temporal['Ticker'][13]:W[:,1],
                               tabla_temporal['Ticker'][2]:W[:,2],
                               tabla_temporal['Ticker'][0]:W[:,3],
                               tabla_temporal['Ticker'][25]:W[:,4],
                               tabla_temporal['Ticker'][4]:W[:,5],
                               tabla_temporal['Ticker'][29]:W[:,6],
                               tabla_temporal['Ticker'][8]:W[:,7],
                               tabla_temporal['Ticker'][24]:W[:,8],
                               tabla_temporal['Ticker'][11]:W[:,9],
                               tabla_temporal['Ticker'][23]:W[:,10],
                               tabla_temporal['Ticker'][19]:W[:,11],
                               tabla_temporal['Ticker'][22]:W[:,12],
                               tabla_temporal['Ticker'][10]:W[:,13],
                               tabla_temporal['Ticker'][6]:W[:,14],
                               tabla_temporal['Ticker'][1]:W[:,15],
                               tabla_temporal['Ticker'][20]:W[:,16],
                               tabla_temporal['Ticker'][18]:W[:,17],
                               tabla_temporal['Ticker'][27]:W[:,18],
                               tabla_temporal['Ticker'][26]:W[:,19],
                               tabla_temporal['Ticker'][28]:W[:,20],
                               tabla_temporal['Ticker'][3]:W[:,21],
                               tabla_temporal['Ticker'][9]:W[:,22],
                               tabla_temporal['Ticker'][21]:W[:,23],
                               tabla_temporal['Ticker'][30]:W[:,24],
                               tabla_temporal['Ticker'][14]:W[:,25],
                               tabla_temporal['Ticker'][15]:W[:,26],
                               tabla_temporal['Ticker'][5]:W[:,27],
                               tabla_temporal['Ticker'][17]:W[:,28],
                               tabla_temporal['Ticker'][7]:W[:,29],
                               tabla_temporal['Ticker'][12]:W[:,30],
                               'Media':Erp,
                               'Vol':sp,
                               'RS':RS})

# Portafolio EMV
port_EMV_montecarlo = np.round(portafolios[portafolios['RS']==portafolios['RS'].max()],6)
ponderaciones_montecarlo = port_EMV_montecarlo.iloc[:,:31]

cash_activo = (1-tabla_temporal['Pesos'].sum())*capital
disp_inv_ini_activo = capital - cash_activo

precios_filtrado = precios.iloc[12:,]

#---------------------------------------------------------------------------------------------------------------------------------------------------#

#creacion de tablas

df_activa = pd.DataFrame(columns=columnas1, index=filas1).reset_index() 
df_activa['Rendimiento']=0
df_activa['Rendimiento acumulado']=0
df_activa['Valor portafolio']=capital

columnas2 = ['Titulos totales','Titulos compra','Titulos venta','Comisión','Comisión acum']
df_operaciones = pd.DataFrame(columns=columnas2, index=filas1).reset_index() 
df_operaciones['Titulos totales']=0
df_operaciones['Titulos compra']=0
df_operaciones['Comisión']=0
df_operaciones['Comisión acum']=0
df_operaciones['Titulos venta']=0

columnas3=['Medida','Descripción','Inv activa', 'Inv pasiva']
df_medidas = pd.DataFrame(columns=columnas3)
df_medidas['Medida'] = ['rend_m', 'rend_c', 'sharpe']
df_medidas['Descripción'] = ['Rendimiento Promedio Mensual', 'Rendimiento mensual acumulado', 'Sharpe Ratio']

#---------------------------------------------------------------------------------------------------------------------------------------------------#

#Simulación de portafolio activo

#precios_periodo_total = yf.download(tabla_temporal['Ticker'].to_list(), start = "2021-01-29", end = "2023-01-26")['Close'].reset_index()
#precios_periodo_total.to_csv('../files/precios_periodo_total.csv')

precios_periodo_total = pd.read_csv('../files/precios_periodo_total.csv')
precios_periodo_total.drop(['Unnamed: 0'], axis=1, inplace=True)

#Creacion de portafolio inicial (2022-01-26), condiciones iniciales

tabla_temporal_2 = pd.DataFrame(columns=columnas, index=filas).reset_index()  
tabla_temporal_2.rename(columns={'index':'Ticker'}, inplace=True)
tabla_temporal_2.sort_values('Ticker', inplace=True)
tabla_temporal_2['Pesos'] = ponderaciones_montecarlo.squeeze().values
tabla_temporal_2['Dinero destinado'] = tabla_temporal_2['Pesos']*disp_inv_ini_activo
tabla_temporal_2['Precio'] = precios_filtrado.iloc[0,1:].to_list()
tabla_temporal_2['Titulos'] = np.round(tabla_temporal_2['Dinero destinado']/tabla_temporal_2['Precio'],0)
tabla_temporal_2['Capital Real destinado'] = tabla_temporal_2['Precio'] * tabla_temporal_2['Titulos']
tabla_temporal_2['Comision individual'] = tabla_temporal_2['Titulos']*tabla_temporal_2['Precio']*.00125
cash_activo =  capital - tabla_temporal_2['Capital Real destinado'].sum() - tabla_temporal_2['Comision individual'].sum()
df_operaciones['Titulos totales'][12]=tabla_temporal_2['Titulos'].sum()
df_operaciones['Titulos compra'][12] = tabla_temporal_2['Titulos'].sum()
df_operaciones['Comisión'][12] = tabla_temporal_2['Comision individual'].sum()
df_activa['Valor portafolio'][12] = tabla_temporal_2['Capital Real destinado'].sum() + cash_activo

rends = precios_filtrado.iloc[:,1:].pct_change().dropna()
tabla_movimientos = pd.DataFrame(tabla_temporal_2)
tabla_movimientos.drop(['Pesos','Dinero destinado','Comision individual','Capital Real destinado',
       'Comision individual'], axis=1,inplace=True)
tabla_movimientos['Comision individual']=0

#Pre Proceso de venta

#cambiar formatos de columnas
df_operaciones['Comisión']=pd.to_numeric(df_operaciones['Comisión'], downcast='float')


tabla_movimientos=tabla_movimientos.reset_index() 

#Pre proceso de compra
rends_dia_antes = precios_periodo_total.set_index('Date')
rends_dia_antes = rends_dia_antes.pct_change().dropna().reset_index() 
rends_dia_antes = rends_dia_antes[ 
        (rends_dia_antes['Date'] == '2022-02-25')| 
        (rends_dia_antes['Date'] == '2022-03-30')| 
        (rends_dia_antes['Date'] == '2022-04-28')| 
        (rends_dia_antes['Date'] == '2022-05-30')| 
        (rends_dia_antes['Date'] == '2022-06-29')| 
        (rends_dia_antes['Date'] == '2022-07-28')| 
        (rends_dia_antes['Date'] == '2022-08-30')| 
        (rends_dia_antes['Date'] == '2022-09-29')| 
        (rends_dia_antes['Date'] == '2022-10-28')| 
        (rends_dia_antes['Date'] == '2022-11-29')| 
        (rends_dia_antes['Date'] == '2022-12-29')| 
        (rends_dia_antes['Date'] == '2023-01-24')]


j=0 #Contador de periodos

for j in range(12):

    #Actualizar precios en tabla de movimientos
    tabla_movimientos['Precio'] = precios_filtrado.iloc[j+1:j+2,1:].squeeze().values
    
    #Parte de venta
    #----------------------------------------------------------------------------------------------------------------------------#
    conta=0
    for i in(rends.columns):
        
        if (rends[i].iloc[j]) <= .05:
            
            titulos_venta = np.round((tabla_movimientos[tabla_movimientos['Ticker'] == i]['Titulos'].values)*.025,0)
                    
            while (cash_activo>=(tabla_movimientos['Precio'][conta]*.00125)) and  titulos_venta[0]!=0 :
                        
                df_operaciones['Titulos venta'][j+13] += 1
                df_operaciones['Comisión'][j+13] += tabla_movimientos['Precio'][conta] * 0.00125
                titulos_venta[0] -= 1
                cash_activo -= tabla_movimientos['Precio'][conta] * 0.00125 + tabla_movimientos['Precio'][conta]
                tabla_movimientos['Titulos'][conta] -= 1
            
        conta+=1
    #----------------------------------------------------------------------------------------------------------------------------#
    #Parte de compra
        
    u=pd.DataFrame(rends_dia_antes.iloc[j,j+1:]).reset_index()
    u = u.set_axis(['Ticker','cambio'], axis=1).sort_values('cambio',ascending=False)
    
    conta=0
    for i in(u['Ticker']):
        
            if (rends[i].iloc[j]) >= .05:
                
                titulos_compra = np.round((tabla_movimientos[tabla_movimientos['Ticker'] == i]['Titulos'].values)*.025,0)
                
                while (cash_activo>=(tabla_movimientos['Precio'][conta]*.00125)) and  titulos_compra[0]!=0 :
                    
                    df_operaciones['Titulos compra'][j+13] += 1
                    df_operaciones['Comisión'][j+13] += tabla_movimientos['Precio'][conta] * 0.00125
                    titulos_compra[0] -= 1
                    tabla_movimientos['Titulos'][conta] += 1
                    cash_activo -= tabla_movimientos['Precio'][conta] * 0.00125 - tabla_movimientos['Precio'][conta] 
            conta+=1
     
    #----------------------------------------------------------------------------------------------------------------------------#
    
    df_operaciones['Titulos totales'][j+13] = df_operaciones['Titulos totales'][j+12] + df_operaciones['Titulos compra'][j+13] - df_operaciones['Titulos venta'][j+13]
    df_activa['Valor portafolio'][j+13] = sum(tabla_movimientos['Titulos']*tabla_movimientos['Precio'])+cash_activo
    
df_activa['Rendimiento']=pd.to_numeric(df_activa['Rendimiento'], downcast='float')  
df_activa['Rendimiento acumulado']=pd.to_numeric(df_activa['Rendimiento acumulado'], downcast='float')
df_operaciones['Comisión acum']=pd.to_numeric(df_operaciones['Comisión acum'], downcast='float')    

for i in range(13):
    df_operaciones['Comisión acum'][i+12] =  df_operaciones['Comisión acum'][i+11] + df_operaciones['Comisión'][i+12]
    df_activa['Rendimiento'][i+12] = (df_activa['Valor portafolio'][i+12]/df_activa['Valor portafolio'][i+11])-1
    df_activa['Rendimiento acumulado'][i+12] = df_activa['Rendimiento acumulado'][i+11] + df_activa['Rendimiento'][i+12]

df_medidas['Inv activa'][0] = df_activa["Rendimiento"].iloc[11:].mean()
df_medidas['Inv pasiva'][0] = df_pasiva["Rendimiento"].mean()

df_medidas['Inv activa'][1] = df_activa["Rendimiento acumulado"][24]
df_medidas['Inv pasiva'][1] = df_pasiva["Rendimiento acumulado"][24]

df_medidas['Inv activa'][2] = (df_activa["Rendimiento"].iloc[11:].mean() - (rf/12)) / df_activa["Rendimiento"].iloc[11:].std()
df_medidas['Inv pasiva'][2] = (df_pasiva["Rendimiento"].mean() - (rf/12)) / df_pasiva["Rendimiento"].std()
