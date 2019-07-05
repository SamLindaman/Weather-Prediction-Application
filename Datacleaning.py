#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: anton
"""

import pandas as pd
from datetime import datetime
from dateutil import parser


data_raw = pd.read_csv('/users/anton/downloads/1793683.csv',encoding='utf-8')

#print(data_rw) //printing out the read file

data_raw['date']=data_raw['DATE'].apply(parser.parse)
data_raw['tmax']=data_raw['TMAX'].astype(float)
data_raw['tmin']=data_raw['TMIN'].astype(float)

data = data_raw.loc[:,['date','tmax','tmin']]

data = data[(pd.Series.notnull(data['tmax'])) & (pd.Series.notnull(data['tmin']))]

data =data[(data['date']>= datetime(1997,1,1)) & (data['date']<=datetime(2019,6,1))]
#data.query("date.dt.day ==30 & date.dt.month == 12", inplace = True) //if one wants to query specific dates

data.to_csv('cleanedData.csv',index = None)

