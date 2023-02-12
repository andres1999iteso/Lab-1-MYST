# -*- coding: utf-8 -*-
 
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime

def remove_mean(data):
    return data-np.mean(data)

def add_number(data, number):
    return data+number 

def read_tables(filename):
    return pd.read_csv(filename,header=2).dropna(subset=['Nombre'])

def prices(tickers,start_date, end_date, fechas_consulta):
    
    matriz = yf.download(tickers, start = start_date, end = end_date)['Close']
    matriz = matriz.reset_index()    
    matriz["Coincidencia"] = False

    for i in (fechas_consulta):
        for j in range(len(matriz)):
            if (matriz["Date"][j]) ==  i:
               matriz["Coincidencia"][j] = True  
    
    final=matriz[matriz['Coincidencia'] == True]
    final.drop(['Coincidencia'], axis=1, inplace=True)
    
    return final


def prices_daily(tickers, start_date=None, end_date=None):
    
    matriz = yf.download(tickers, start = start_date, end = end_date)['Close']
    log_ret = np.log(matriz/matriz.shift()).dropna()
    rend=log_ret.mean()*252
    desv=log_ret.std()*(252**.5)
    
    return rend,desv,log_ret

# Función objetivo
def varianza(w,Sigma):
    return w.T.dot(Sigma).dot(w)

# Función objetivo
def menos_RS(w,Eind,Sigma,rf):
    Ep=Eind.T.dot(w)
    sp=(w.T.dot(Sigma).dot(w))**.5
    RS=(Ep-rf)/sp
    return -RS



