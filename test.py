import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
from datetime import date
from graphdata import get_graph_data
import plotly.graph_objs as go

#df = pd.read_excel('/home/daksh/Main/Clearmind/Clearmind Dashboard/data/BO2_STRATEGY.xlsx')
#df = df.drop(df.iloc[:,5:13],axis = 1)
#
#df[['Day','Month','Year']] = df.Date.str.split("-",expand = True)
#
#date_list = []
#for row in df.index:
#    date_list.append(date(int(df['Year'][row]),int(df['Month'][row]),int(df['Day'][row])))
#
#df['Date'] = date_list
#
#df['Buy'] = df["Type"] == "BUY TRADE"
#df['Sell'] = df["Type"] == "SELL TRADE"
#
#plt.plot(df['Date'], df['Price'],linewidth=1,color='black')
#plt.scatter(df.loc[df['Buy'] ==1 , 'Date'].values,df.loc[df['Buy'] ==1, 'Price'].values, label='skitscat', color='green', s=25, marker="^")
#plt.scatter(df.loc[df['Sell'] ==1 , 'Date'].values,df.loc[df['Sell'] ==1, 'Price'].values, label='skitscat', color='red', s=25, marker="v")
#
#plt.xlabel('Date')  
#plt.ylabel('Price')  

#strategy_name = ["LTF1","LTF2","LTF3"]
#strategy_type = "Simple"
#
#dff = get_graph_data(strategy_name,strategy_type,10000)
dff = pd.read_csv(os.path.join(os.getcwd(),"test.csv"))
dff = dff.drop(dff.iloc[:,6:13], axis = 1)


test = {}

list_names = dff["Ticker"].unique().tolist()

fig = go.Figure()

