import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly
import plotly.express as px
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go
from graphdata import get_graph_data
from prarameters import get_stratagy_parameters
from prarameters import empty_parameter_df
from backtest_only import backtest


def get_backtest(ticker_options,strategy_options):
    df = pd.DataFrame()
    
    flag = True
    
    if flag:
        df = backtest(ticker_options,strategy_options)
        flag = False
    else:
        list_names = df["Ticker"].unique().tolist()
        if list_names != ticker_options:
            df = backtest(ticker_options,strategy_options)
    return df



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#importing strategy report csv
#df_strategy_report = pd.read_csv("/home/daksh/Main/Clearmind/Clearmind Dashboard/strategy_report.csv")
#df_strategy_report = df_strategy_report.drop(columns = ["date"])

df_strategy_report = empty_parameter_df()

#importing ticker options
df_ticker_options = pd.read_csv("/home/daksh/Main/Clearmind/Clearmind Dashboard/ticker_options.csv")

#importing strat option
df_strat_options = pd.read_excel("/home/daksh/Main/Clearmind/Clearmind Dashboard/strat_names.xlsx")

ticker_options = [
    {"label": str(df_ticker_options['name'][row]), "value": str(df_ticker_options['name'][row])}
    for row in df_ticker_options.index
]

strategy_options = [
    {"label": str(df_strat_options['Name'][i]), "value": df_strat_options['Name'][i]}
    for i in df_strat_options.index
]

report_options = [
    {"label": str(df_strategy_report.columns[j]), "value": str(df_strategy_report.columns[j])}
    for j in range(df_strategy_report.shape[1])
]


app.layout = html.Div(children=[
            dcc.Store(id="aggregate_data"),
            html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("logo.jpeg"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Clear Mind",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Strategy Analysis", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
            html.Div(
            [
                html.Div(
                    [
                        html.P("Select Type"),
                        dcc.RadioItems(
                            id = "analysis_type",
                            options=[
                                {'label': 'Single Single', 'value': 'SS'},
                                {'label': 'Multi Ticker Sting Strat ', 'value': 'MS'},
                                {'label': 'Single Start Multi Ticker', 'value': 'SM'}
                            ],
                            value='SS',
                            labelStyle={'display': 'inline-block'},

                        ), 
                        html.P("Select Ticker", className="control_label"),
                        dcc.Dropdown(
                            id="ticker_options",
                            options=ticker_options,
#                            multi=False,
                            value=df_ticker_options["name"][0],
#                            value=list(WELL_STATUSES.keys()),
                            className="dcc_control",
                            clearable = False,
                        ),
                        html.P("Select Strategy:", className="control_label"),
                        dcc.Dropdown(
                            id="strategy_name",
                            options=strategy_options,
#                            multi=False,
                            value=df_strat_options["Name"][0],
                            className="dcc_control",
                            clearable = False,
                        ),
                        dcc.RadioItems(
                            id = "strategy_type",
                            options=[
                                {'label': 'Points-In', 'value': 'Points-In'},
                                {'label': 'Simple', 'value': 'Simple'},
                                {'label': 'Compound', 'value': 'Compound'}
                            ],
                            value='Simple',
                            labelStyle={'display': 'inline-block'},

                        ), 
                        html.P("Select Report Parameters:", className="control_label"),
                        dcc.Dropdown(
                            id="report_columns",
                            options=report_options,
                            multi=True,
                            value="ticker_name",
                            className="dcc_control",
                            clearable = False,

                        ),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="opening_text"), html.P("Opening Balance")],
                                    id="opening",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="closing_text"), html.P("Closing Balaace")],
                                    id="closing",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="pnl_text"), html.P("Pnl")],
                                    id="pnl",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="pnl_percent_text"), html.P("Pnl Percentage")],
                                    id="pnl_percent",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="profit-loss")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                dcc.Store(id="selected-rows", storage_type="memory"),
                html.Div(id="tables-container"),
                html.Div(
                    children = dash_table.DataTable(
                            id = "Table",
                            columns = [{"name": i, "id": i} for i in df_strategy_report.columns],
                            style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                    }
                                ],
                            style_header={
                                    'backgroundColor': 'rgb(230, 230, 230)',
                                    'fontWeight': 'bold'
                                }
                            )
                        )
            ],
            className="row flex-display",
        ),
])

#@app.callback(
#        [   
#            Output("opening_text", "children"),
#            Output("closing_text", "children"),
#            Output("pnl_text", "children"),
#            Output("pnl_percent_text", "children"),
#            ],
#        [
#         Input("strategy_name","value")
#            ],
#        )
#def update_text(strategy_name):
#    open_balance = 10000
#    for strat_index in df_strategy_report.index:
#        if(df_strategy_report['stratgy_name'][strat_index] == strategy_name):
#            break
#    close_balance = df_strategy_report['value_at_end'][strat_index]
#    pnl = df_strategy_report['profit_loss'][strat_index]
#    pnl_percentage = df_strategy_report['roe'][strat_index]
#    return "₹" + str(open_balance), "₹" + str(close_balance), "₹" + str(pnl), str(pnl_percentage) + "%"

#Call back for choosing anaysis approach
@app.callback([
            Output('ticker_options','multi'),
            Output('strategy_name','multi'),
            ],
              [
            Input('analysis_type','value')
            ]
        )

def analysis_approach(analysis_type):
    if analysis_type == "SS":
        return False, False
    elif analysis_type == "MS":
        return True, False
    else:
        return False, True
     
        
@app.callback([
            Output('profit-loss', 'figure'),
            Output('Table', 'data'),           
        ],
              [
          Input('ticker_options','value'),
          Input('strategy_name','value'),
          Input('strategy_type','value'),
          Input('analysis_type','value')
        ],
        )

def run_strat_on_ticker(ticker_options,strategy_name,strategy_type,analysis_type):

    
    df_backtest = get_backtest(ticker_options,strategy_name)
    
    fig = update_graph_scatter(df_backtest,ticker_options,strategy_name,strategy_type,analysis_type)
    
    table = update_rows(df_backtest,ticker_options,strategy_name,strategy_type)
    
    return fig,table
#Call back for updating graph        
#@app.callback(
#        Output('profit-loss', 'figure'),
#     [
#      Input('ticker_options','value'),
#      Input('strategy_name','value'),
#      Input('strategy_type','value'),
#      ],
#)


def update_graph_scatter(df_backtest,ticker_options,strategy_name,strategy_type,analysis_type):
    
    if isinstance(strategy_name,str) and isinstance(ticker_options,str):
        strat = str(strategy_name) + " " + str(strategy_type)
#        dff = df_strategy_graph[df_strategy_graph["stratgy_name"].isin([strat])]
        dff = get_graph_data(df_backtest,ticker_options,strategy_name,strategy_type,10000)

        # print(dff[:5])
        fig = go.Figure()

        fig.add_trace(go.Scatter(
                        x=dff["close_date"].values, 
                        y=dff["value"].values, 
#                        color='name', 
                        mode = "lines"
                        )
                    )
        fig.add_trace(go.Scatter(   
                        x = dff["open_date"].values,
                        y = dff["value"].values,
                        mode = "markers",
                        marker = dict(
                            color = "rgb(0,255,0)",
                            symbol = 5,
                            ),
                        name = str(dff["strat"][1] + " Open Date")
                        )
                    )

        fig.add_trace(go.Scatter(   
                        x = dff["close_date"].values,
                        y = dff["value"].values,
                        mode = "markers",
                        marker = dict(
                            color = "rgb(255,0,0)",
                            symbol = 6,

                            ),
                        name = str(dff["strat"][1] + " Close Date")
                        )
                    )
                        
        return fig
    strat = []
    for row in range(len(strategy_name)):
        strat.append(str(strategy_name[row]) + " " + str(strategy_type))
    dff = get_graph_data(df_backtest,ticker_options,strategy_name,strategy_type,10000)
#    dff = df_strategy_graph[df_strategy_graph["stratgy_name"].isin(strat)]
        # print(dff[:5])
    print(dff)    
    if analysis_type == "SS":
        list_names = dff["strat"].unique().tolist()
        column = "strat"
    elif analysis_type == "MS":
        list_names = dff["ticker"].unique().tolist()
        column = "ticker"

    else:
        list_names = dff["strat"].unique().tolist()

    fig = go.Figure()

    for ticker_name in list_names:
        fig.add_trace(go.Scatter(
                            x=dff.loc[dff[column] ==ticker_name , 'close_date'].values, 
                            y=dff.loc[dff[column] ==ticker_name , 'value'].values,
    #                        color='name', 
                            mode = "lines",
                            name = ticker_name 
                            )
                        )
        fig.add_trace(go.Scatter(   
                            x = dff.loc[dff[column] ==ticker_name , 'open_date'].values,
                            y = dff.loc[dff[column] ==ticker_name , 'value'].values,
                            mode = "markers",
                            marker = dict(
                                color = "rgb(0,255,0)",
                                symbol = 5
                                ),
                            name = str(ticker_name + " Open Date")
                            )                   
                        ) 

    
        fig.add_trace(go.Scatter(   
                            x = dff.loc[dff[column] ==ticker_name , 'close_date'].values,
                            y = dff.loc[dff[column] ==ticker_name , 'value'].values,
                            mode = "markers",
                            marker = dict(
                                color = "rgb(255,0,0)",
                                symbol = 6
                                ),
                            name = str(ticker_name + " Close Date")
                            )
                        ) 
                

    fig.update_layout(title={'text':'Portfolio Value',
                     'font':{'size':28},'x':0.5,'xanchor':'center'})
    
    print(dff.info())
    return fig
            
#@app.callback(Output('Table', 'data'),
#              [
#                Input("ticker_options","value"),
#                Input("strategy_name","value"),
#                Input("strategy_type","value")
#                ]
#              )
#def update_parameters(ticker_options,strategy_name,strategy_type):
#    df_strategy_report = get_stratagy_parameters(ticker_options,strategy_name,strategy_type,10000)
#    


#@app.callback(          
#             Output('Table', 'data'),           
#             [
#                 Input("ticker_options","value"),    
#                 Input('strategy_name','value'),
#                 Input('strategy_type','value'),
#             ])
#      
                  
def update_rows(df_backtest,ticker_options,strategy_name,strategy_type):   

    df_strategy_report = get_stratagy_parameters(df_backtest,ticker_options,strategy_name,strategy_type,10000)
    if isinstance(strategy_name,str): 
        strat = str(strategy_name) + " " + str(strategy_type)
        dff = df_strategy_report[df_strategy_report['stratgy_name'] == strat]
        dff_dict = dff.to_dict('records')
        return dff_dict
    strat = []
    for row in range(len(strategy_name)):
        strat.append(str(strategy_name[row]) + " " + str(strategy_type)) 
    dff = df_strategy_report[df_strategy_report['stratgy_name'].isin(strat)]
    dff_dict = dff.to_dict('records')
    return dff_dict


@app.callback(Output('Table', 'columns'),
            [
             Input('report_columns','value'),
            ])
def update_columns(report_columns):
    
    if isinstance(report_columns,str): 
        columns = [{"name": df_strategy_report.columns[0], "id": df_strategy_report.columns[0]}]
        return columns
    
    col_index = []
    for col in range(len(report_columns)):    
        col_index.append(df_strategy_report.columns.get_loc(report_columns[col]))
    columns = [{"name": df_strategy_report.columns[col_index[k]], "id": df_strategy_report.columns[col_index[k]]} for k in range(len(col_index))]
    return columns


if __name__ == "__main__":
    app.run_server(debug = True)
    















