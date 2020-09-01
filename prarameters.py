import pandas as pd
import time
from csv import DictWriter
from datetime import date
from backtest_only import backtest


def append_dict_as_row(file_name, dict_of_elem, field_names):
    with open(file_name, 'a+', newline='') as write_obj:
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        dict_writer.writerow(dict_of_elem)


def pointsin(pnl_list):
    cumm_pnl = sum(pnl_list)
    max_trade_return = max(pnl_list)
    return cumm_pnl, max_trade_return

def simple(simple_capital,buy_trade_price,sell_trade_price):
#   inital capital is the ammount to be used during buy trades
    inital_capital = simple_capital
    simple_qty = []
    simple_profit = []
    simple_loss = []
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
            simple_loss.append(loss)
            simple_capital = simple_capital + loss
    cumm_sum = sum(simple_profit) if len(simple_profit) !=0 else sum(simple_loss) if len(simple_loss) !=0 else 0
    max_trade_return = max(simple_profit) if len(simple_profit) != 0 else 0
    return cumm_sum, max_trade_return

def _complex(initial_capital,buy_trade_price,sell_trade_price):
    compound_capital = initial_capital
    compound_qty = []
    compound_post_sell = []
    compound_cumm_profit = []
    for row in range(len(buy_trade_price)):
        compound_qty.append(int(compound_capital/buy_trade_price[row]))
        x = compound_capital - (compound_qty[row]*buy_trade_price[row])
        compound_post_sell.append(int(compound_qty[row] * sell_trade_price[row]))
        compound_capital = compound_post_sell[row] + x
        compound_cumm_profit.append(compound_capital - initial_capital)
    
    cumm_sum = compound_cumm_profit[-1]
    max_trade_return = max(compound_post_sell) if len(compound_post_sell) != 0 else 0
    return cumm_sum, max_trade_return
    

def stratagy_parameters(df,df_backtest,ticker_name,strat_name,strat_approach,initial_value):
    
    df = pd.DataFrame(columns = ['ticker_name','stratgy_name','profit_loss','value_at_end','CAGR','no_of_buy','no_of_sell',
                             'no_of_bars_in','avg_trade_return','max_drawdown',"no_of_buy_orders","no_of_sell_orders",
                             "max_trade_return", "roe", "position_status"])

    df_strart_excel = df_backtest[df_backtest["Ticker"]==ticker_name]
#    df_strart_excel = pd.read_excel("/home/daksh/Main/Clearmind/Clearmind Dashboard/data/"+strat_name+"_STRATEGY.xlsx")
    df_strart_excel = df_strart_excel.drop(df_strart_excel.iloc[:,5:13], axis = 1)
    
    df_strart_excel[['Day','Month','Year']] = df_strart_excel.Date.str.split("-",expand = True)
    
    no_of_calls = df_strart_excel['Type'].value_counts()
    
    open_date = []
    close_date = []
    buy_trade_price = []
    sell_trade_price = []
    
    for row in df_strart_excel.index:
        if df_strart_excel.Type[row] == 'BUY TRADE':
            open_date.append(date(int(df_strart_excel['Year'][row]),int(df_strart_excel['Month'][row]),int(df_strart_excel['Day'][row])))
            buy_trade_price.append(df_strart_excel['Price'][row])
        
        if df_strart_excel.Type[row] == 'SELL TRADE':
            close_date.append(date(int(df_strart_excel['Year'][row]),int(df_strart_excel['Month'][row]),int(df_strart_excel['Day'][row])))
            sell_trade_price.append(df_strart_excel['Price'][row])
    
    if len(open_date) == len(close_date):
        positon_status = "Close"
    else:
        positon_status = "Open"
    
    pnl_list = []
    for call in range(len(buy_trade_price)):
        pnl = 0
        pnl = sell_trade_price[call] - buy_trade_price[call]
        pnl_list.append(pnl)
    
    
    if strat_approach == "Points-In":
        cumm_pnl,max_trade_return = pointsin(pnl_list)
    elif strat_approach == "Simple":
        cumm_pnl,max_trade_return = simple(initial_value,buy_trade_price,sell_trade_price)
    elif strat_approach == "Compound":
        cumm_pnl,max_trade_return = _complex(initial_value,buy_trade_price,sell_trade_price)
    else:
        print("Invalid strategy Approach") 

    no_of_bars_in_list = []
    for row_date in range(len(open_date)):   
        no_of_days = close_date[row_date] - open_date[row_date]
        no_of_bars_in_list.append(no_of_days.days/7)
    
    no_of_years = int(df_strart_excel['Year'].iloc[-1]) - int(df_strart_excel['Year'].iloc[0])       
    df_pnl_list = pd.DataFrame(pnl_list, columns = ["Value"]) 
    df_cumm = pd.DataFrame(columns = ["Cumm","DD"])
    df_cumm['Cumm'] = df_pnl_list['Value'].cumsum()
    Roll_Max = df_cumm['Cumm'].cummax()
    Daily_Drawdown = Roll_Max - df_cumm['Cumm']
    df_cumm['DD'] = Daily_Drawdown     
    
    stime = time.gmtime()
    run_date = date(stime[0],stime[1],stime[2])    
    
    stratgy_name = str(strat_name) +" "+ str(strat_approach)
#    cumm_pnl = sum(pnl_list)
    value_at_end = initial_value + cumm_pnl
    CAGR = ((((initial_value + cumm_pnl)/initial_value)**(1/no_of_years)) - 1)*100
    no_buy_trades = no_of_calls[2]
    no_sell_trades = no_of_calls[3]
    no_of_bars_in = sum(no_of_bars_in_list)
    avg_return_trade = cumm_pnl/no_sell_trades
    max_drawdown = max(Daily_Drawdown)       
    no_buy_orders = no_of_calls[1]
    no_sell_orders = no_of_calls[0]
#    max_trade_return = max(pnl_list)
#    max_trade_return_percent = 0
    roe = (cumm_pnl/initial_value) * 100
        
#    field_names = ['date',
#                   'stratgy_name',
#                   'profit_loss',
#                   'value_at_end',
#                   'CAGR',
#                   'no_of_buy',
#                   'no_of_sell',
#                   'no_of_bars_in',
#                   'avg_trade_return',
#                   'max_drawdown',
#                   "no_of_buy_orders",
#                   "no_of_sell_orders",
#                   "max_trade_return",
#                   "roe",
#                   "position_status"]
    
    row_dict = {'ticker_name':ticker_name,
                'stratgy_name': stratgy_name,
                'profit_loss':"{:.2f}".format(cumm_pnl),
                'value_at_end':"{:.2f}".format(value_at_end),
                'CAGR': "{:.2f}".format(CAGR),
                'no_of_buy': no_buy_trades,
                'no_of_sell': no_sell_trades,
                'no_of_bars_in':  no_of_bars_in,
                'avg_trade_return':"{:.2f}".format(avg_return_trade),
                'max_drawdown':"{:.2f}".format(max_drawdown), 
                "no_of_buy_orders":no_buy_orders,
                "no_of_sell_orders":no_sell_orders,
                "max_trade_return":"{:.2f}".format(max_trade_return),
                "roe":"{:.2f}".format(roe),
                "position_status":positon_status}
#    append_dict_as_row("/home/daksh/Main/Clearmind/CSVs/strategy_report.csv", row_dict, field_names)
 
    df_temp = pd.DataFrame([row_dict], columns = row_dict.keys())
    df = pd.concat([df, df_temp], axis = 0).reset_index()
    return df
     

def get_stratagy_parameters(df_backtest,ticker_name,strat_name,strat_approach,initial_value):
    
    df = pd.DataFrame()    
    df_temp = pd.DataFrame()
    
    if isinstance(ticker_name, list):
        list_ticker_name = ticker_name           
        for row in range(len(list_ticker_name)):
            df_temp = stratagy_parameters(df,df_backtest,list_ticker_name[row],strat_name,strat_approach,initial_value)
            df = df.append(df_temp)
        return df   
    elif isinstance(strat_name,str):
        df = stratagy_parameters(df,df_backtest,ticker_name,strat_name,strat_approach,initial_value)
    else:
        list_strat_name = strat_name           
        for row in range(len(list_strat_name)):
          df_temp = stratagy_parameters(df,df_backtest,ticker_name,list_strat_name[row],strat_approach,initial_value)            
          df = df.append(df_temp)
    return df


def empty_parameter_df():
    df = pd.DataFrame(columns = ['ticker_name','stratgy_name','profit_loss','value_at_end','CAGR','no_of_buy','no_of_sell',
                             'no_of_bars_in','avg_trade_return','max_drawdown',"no_of_buy_orders","no_of_sell_orders",
                             "max_trade_return", "roe", "position_status"])
    return df

#dff = pd.DataFrame()
#ticker = ('MICR.BO')
#strat = ["LTF12","LTF11"]
#dff = get_stratagy_parameters(ticker,strat,"Compound",10000)
#print(dff.head())

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#    
