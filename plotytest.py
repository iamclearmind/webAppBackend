import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from datetime import date
from graphdata import get_graph_data
import plotly.graph_objects as go
df = pd.read_excel('/home/daksh/Main/Clearmind/Clearmind Dashboard/data/BO2_STRATEGY.xlsx')
df = df.drop(df.iloc[:,5:13],axis = 1)

df[['Day','Month','Year']] = df.Date.str.split("-",expand = True)

date_list = []
for row in df.index:
    date_list.append(date(int(df['Year'][row]),int(df['Month'][row]),int(df['Day'][row])))

df['Date'] = date_list

df['Buy'] = df["Type"] == "BUY TRADE"
df['Sell'] = df["Type"] == "SELL TRADE"

buy_date = []
sell_date = []

for row in df.index:
    if df['Buy'][row]:
        buy_date.append(df['Date'][row])
    elif df['Sell'][row]:
        sell_date.append(df['Date'][row])
        
fig = go.Figure()

fig.add_trace(go.Scatter(   
        x = df.loc[df['Buy'] ==1 , 'Date'].values,
        y = df.loc[df['Buy'] ==1, 'Price'].values,
        mode = "markers",
        marker = dict(
            color = "rgb(0,255,0)",
            symbol = 5
            )
        )) 


fig.add_trace(go.Scatter(   
        x = df.loc[df['Sell'] ==1 , 'Date'].values,
        y = df.loc[df['Sell'] ==1, 'Price'].values,
        mode = "markers",
        marker = dict(
            color = "rgb(255,0,0)",
            symbol = 6 
        )
        )) 

fig.update_layout(
        showlegend=False,
        annotations=[
        dict(
            x= df.loc[df['Buy'] ==1 , 'Date'].values,
            y= df.loc[df['Buy'] ==1, 'Price'].values,
            xref="x",
            yref="y",
            text="Test",
#            showarrow=True,
#            arrowhead=7,
#            ax=0,
#            ay=-40
        )
    ])

fig.show()
#plt.plot(df['Date'], df['Price'],linewidth=1,color='black')
#plt.scatter(df.loc[df['Buy'] ==1 , 'Date'].values,df.loc[df['Buy'] ==1, 'Price'].values, label='skitscat', color='green', s=25, marker="^")
#plt.scatter(df.loc[df['Sell'] ==1 , 'Date'].values,df.loc[df['Sell'] ==1, 'Price'].values, label='skitscat', color='red', s=25, marker="v")
#
#plt.xlabel('Date')  
#plt.ylabel('Price')  











