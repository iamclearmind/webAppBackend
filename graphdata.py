import pandas as pd
from datetime import date
from csv import DictWriter

def append_dict_as_row(file_name, dict_of_elem, field_names):
    with open(file_name, 'a+', newline='') as write_obj:
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        dict_writer.writerow(dict_of_elem)

def pointsin(buy_trade_price,pnl_list,value):
    for row in range(len(buy_trade_price)):
        value.append(value[row] + pnl_list[row])
    return value

def simple(simple_capital,buy_trade_price,sell_trade_price,value):
#   inital capital is the ammount to be used during buy trades
    inital_capital = simple_capital
    simple_qty = []
    simple_profit = []
    for row in range(len(buy_trade_price)):
        simple_qty.append(int(simple_capital/buy_trade_price[row]))
        x = int(simple_qty[row] * sell_trade_price[row])
        y = simple_capital - (simple_qty[row]*buy_trade_price[row])
        simple_capital = simple_capital + y
        if x > inital_capital:
            profit = x - simple_capital
            simple_profit.append(profit)
            simple_capital = inital_capital
        elif x < inital_capital:
            loss = x - simple_capital
            simple_capital = simple_capital + loss
            simple_profit.append(loss)
        value.append(value[row] + simple_profit[row])
 
    return value

def _complex(initial_value,buy_trade_price,sell_trade_price,value):
    compound_capital = initial_value
    compound_qty = []
    compound_post_sell = []
    compound_cumm_profit = []
    for row in range(len(buy_trade_price)):
        compound_qty.append(int(compound_capital/buy_trade_price[row]))
        x = compound_capital - (compound_qty[row]*buy_trade_price[row])
        compound_post_sell.append(int(compound_qty[row] * sell_trade_price[row]))
        compound_capital = compound_post_sell[row] + x
        compound_cumm_profit.append(compound_capital - initial_value)
        value.append(compound_cumm_profit[row] + initial_value)

    return value

def graph_data(df_backtest,ticker_name,strat_name,strat_approach,initial_value,df_return):
#    df_temp = pd.read_excel("/home/daksh/Main/Clearmind/Clearmind Dashboard/data/"+strat_name+"_STRATEGY.xlsx")
    df_temp = df_backtest[df_backtest["Ticker"]==ticker_name]
    df_temp = df_temp.drop(df_temp.iloc[:,5:13], axis = 1)
    
    df_temp[['Day','Month','Year']] = df_temp.Date.str.split("-",expand = True)
        
    open_date = []
    close_date = []
    buy_trade_price = []
    sell_trade_price = []
    close_date = [date(2000,1,1)]
    open_date = [date(2000,1,1)]
    value = [10000]
    
    for row in df_temp.index:
        if df_temp.Type[row] == 'BUY TRADE':
            open_date.append(date(int(df_temp['Year'][row]),int(df_temp['Month'][row]),int(df_temp['Day'][row])))
            buy_trade_price.append(df_temp['Price'][row])
        
        if df_temp.Type[row] == 'SELL TRADE':
            close_date.append(date(int(df_temp['Year'][row]),int(df_temp['Month'][row]),int(df_temp['Day'][row])))
            sell_trade_price.append(df_temp['Price'][row])
    
    pnl_list = []
    for call in range(len(buy_trade_price)):
        pnl = 0
        pnl = sell_trade_price[call] - buy_trade_price[call]
        pnl_list.append(pnl)
    
    if strat_approach == "Points-In":
        value = pointsin(buy_trade_price,pnl_list,value)
        
    elif strat_approach == "Simple":
        value = simple(initial_value,buy_trade_price,sell_trade_price,value)
        
    elif strat_approach == "Compound":
        value = _complex(initial_value,buy_trade_price,sell_trade_price,value)

    strat = str(strat_name) +" "+ str(strat_approach)   
    list_strat = []
    list_ticker = []
    for x in range(len(value)):
        list_ticker.append(ticker_name)
        list_strat.append(strat)
    df = pd.DataFrame({"ticker":list_ticker,
                      "strat": list_strat,
                      "open_date":open_date,
                      "close_date":close_date,
                      "value":value})
    
    df_return = df_return.append(df)
    
    return df_return

#    field_names = ['stratgy_name',
#                   'date',
#                   'value']
#    for row in range(len(open_date)):
#        row_dict = {'stratgy_name':strat,
#                    'date': open_date[row],
#                    'value':value[row]
#                    }
#        append_dict_as_row("/home/daksh/Main/Clearmind/Clearmind Dashboard/stratrgy_graph.csv", row_dict, field_names)

def get_graph_data(df_backtest,ticker_name,strat_name,strat_approach,initial_value):
    dff = pd.DataFrame(columns = ["ticker","strat","open_date","close_date","value"])     
    if isinstance(ticker_name,list):
        list_ticker_name = ticker_name
        for row in range(len(list_ticker_name)):
            dff = graph_data(df_backtest,list_ticker_name[row],strat_name,strat_approach,initial_value,dff)
        return dff 
    elif isinstance(strat_name,str):
        dff = graph_data(df_backtest,ticker_name,strat_name,strat_approach,initial_value,dff)
        return dff
    elif isinstance(strat_name,list):
        list_strat_name = strat_name
        for row in range(len(list_strat_name)):
            df = graph_data(df_backtest,ticker_name,list_strat_name[row],strat_approach,initial_value)
            dff = dff.append(df)
        return dff




        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
#        