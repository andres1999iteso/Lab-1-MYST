# -*- coding: utf-8 -*-

import pandas as pd
import functions as fn
import numpy as np
import yfinance as yf
 
NAFTRAC_20210129=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20210129.csv')
NAFTRAC_20210226=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20210226.csv')
NAFTRAC_20210331=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20210331.csv')
NAFTRAC_20210430=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20210430.csv')
NAFTRAC_20210531=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20210531.csv')
NAFTRAC_20210630=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20210630.csv') 
NAFTRAC_20210730=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20210730.csv')
NAFTRAC_20210831=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20210831.csv')
NAFTRAC_20210930=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20210930.csv')
NAFTRAC_20211026=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20211026.csv')
NAFTRAC_20211130=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20211130.csv')
NAFTRAC_20211231=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20211231.csv')
NAFTRAC_20220126=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20220126.csv')
NAFTRAC_20220228=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20220228.csv')
NAFTRAC_20220331=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20220331.csv')
NAFTRAC_20220429=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20220429.csv')
NAFTRAC_20220531=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20220531.csv')
NAFTRAC_20220630=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20220630.csv')
NAFTRAC_20220729=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20220729.csv')
NAFTRAC_20220831=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20220831.csv')
NAFTRAC_20220930=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20220930.csv')
NAFTRAC_20221031=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20221031.csv')
NAFTRAC_20221130=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20221130.csv')
NAFTRAC_20221230=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20221230.csv')
NAFTRAC_20230125=fn.read_tables('../files/2021-2023_Naftrac/NAFTRAC_20230125.csv')

tickers_fin = pd.read_csv('../files/tickers - corregido.csv')
tickers_fin1 = tickers_fin.iloc[:,1].tolist()
del tickers_fin1[2]

fechas=pd.to_datetime(["2021-01-29","2021-02-26","2021-03-31","2021-04-30","2021-05-31",
        "2021-06-30","2021-07-30","2021-08-31","2021-09-30","2021-10-26",
        "2021-11-30","2021-12-31","2022-01-26","2022-02-28","2022-03-31",
        "2022-04-29","2022-05-31","2022-06-30","2022-07-29","2022-08-31",
        "2022-09-30","2022-10-31","2022-11-30","2022-12-30","2023-01-25"])

precios = fn.prices(tickers_fin1, "2021-01-29" , "2023-01-26" , fechas)
precios.to_csv('../files/precios.csv')

