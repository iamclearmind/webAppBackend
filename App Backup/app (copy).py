import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly

from dash.dependencies import Output, Input, State
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


df_strategy_report = pd.read_csv("/home/daksh/Main/Clearmind/dashboard/dash-web-trader/strategy_report.csv")
df_strategy_report = df_strategy_report.drop(columns = ["date"])
df_ticker_options = pd.read_csv("/home/daksh/Main/Clearmind/dashboard/dash-web-trader/ticker_options.csv")
ticker_options = [
    {"label": str(df_ticker_options['name'][row]), "value": str(df_ticker_options['name'][row])}
    for row in df_ticker_options.index
]


strategy_options = [
    {"label": str(df_strategy_report["stratgy_name"][i]), "value": df_strategy_report["stratgy_name"][i]}
    for i in df_strategy_report.index
]

report_options = [
    {"label": str(df_strategy_report.columns[j]), "value": str(df_strategy_report.columns[j])}
    for j in range(df_strategy_report.shape[1])
]
#def generate_table(dataframe, max_rows=10):
#    return html.Table([
#        html.Thead(
#            html.Tr([html.Th("Strategy Name")])
#        ),
#        html.Tbody([
#            html.Tr([
#                html.Td(dataframe["stratgy_name"][col]) for col in dataframe.index
#            ]) 
#        ])
#    ])


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
                        html.P("Select Ticker", className="control_label"),
                        dcc.Dropdown(
                            id="ticker_options",
                            options=ticker_options,
                            multi=True,
#                            value=list(WELL_STATUSES.keys()),
                            className="dcc_control",
                        ),
#                        dcc.Checklist(
#                            id="lock_selector",
#                            options=[{"label": "Lock camera", "value": "locked"}],
#                            className="dcc_control",
#                            value=[],
#                        ),
                        html.P("Select Strategy:", className="control_label"),
                        dcc.Dropdown(
                            id="strategy_name",
                            options=strategy_options,
                            multi=True,
                            value=df_strategy_report["stratgy_name"][0],
                            className="dcc_control",
                        ),
                        html.P("Select Report Parameters:", className="control_label"),
                        dcc.Dropdown(
                            id="report_columns",
                            options=report_options,
                            multi=True,
                            value=df_strategy_report.columns[0],
                            className="dcc_control",
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
#                            data = df_strategy_report.to_dict('records'),
                            editable = True,
                            row_deletable=True
#                            sorting=True,
#                            sorting_type='multi',
#                            sorting_settings=[],
                            )
                        )
            ],
            className="row flex-display",
        ),
])


@app.callback(
    [   
        Output("opening_text", "children"),
        Output("closing_text", "children"),
        Output("pnl_text", "children"),
        Output("pnl_percent_text", "children"),
    ],
    [
     Input("strategy_name","value")
    ],
)
def update_text(strategy_name):
    open_balance = 10000
    for strat_index in df_strategy_report.index:
        if(df_strategy_report['stratgy_name'][strat_index] == strategy_name):
            break
    close_balance = df_strategy_report['value_at_end'][strat_index]
    pnl = df_strategy_report['profit_loss'][strat_index]
    pnl_percentage = df_strategy_report['roe'][strat_index]
    return "₹" + str(open_balance), "₹" + str(close_balance), "₹" + str(pnl), str(pnl_percentage) + "%"


@app.callback(
        Output('profit-loss', 'figure'),
     [
      Input('strategy_name','value')
      ],
)

def update_graph_scatter(strategy_name):
    df_strategy = pd.read_excel("/home/daksh/Main/Clearmind/dashboard/dash-web-trader/data/"+ str(strategy_name) + "_STRATEGY.xlsx")
    df_strategy = df_strategy.drop(df_strategy.iloc[:,6:13], axis = 1)
    df_strategy['PnL']=df_strategy['PnL'].fillna(0)
    pnl = 10000
    pnl_list = []
    for row in df_strategy.index:
        pnl = pnl + df_strategy['PnL'][row]
        pnl_list.append(pnl)
    df_strategy['pnl_list'] = pnl_list
    X = df_strategy['Date']
    Y = df_strategy['pnl_list']
    data = plotly.graph_objs.Scatter(
            x=X,
            y=Y,
            name='Scatter',
            mode= 'lines+markers'
            )
    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                      yaxis=dict(range=[min(Y),max(Y)]),
                                      title='Term: {}'.format(strategy_name))}

@app.callback(
            
             Output('Table', 'data'), 
#             Output('Table', 'columns')
            
            [
             Input('strategy_name','value'),
            ])
def update_rows(strategy_name):   
    if isinstance(strategy_name,str): 
        dff = df_strategy_report[df_strategy_report['stratgy_name'] == strategy_name]
        dff_dict = dff.to_dict('records')
        return dff_dict
    
    dff = df_strategy_report[df_strategy_report['stratgy_name'].isin(strategy_name)]
    dff_dict = dff.to_dict('records')
    return dff_dict
    print(dff)
    print(strategy_name)
    print(type(strategy_name))

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

#@app.callback(
#    Output("selected-rows", "data"),
#    [Input("report_options", "value")],
#    [State("selected-rows", "data")],
#)
#def display_output(value, storage):
#    if value is not None:
#        return {"selected_rows": df_strategy_report[df_strategy_report["stratgy_name"].str.contains(value)].to_json()}
#
#@app.callback(
#     Output("table", "data"),
#    [
#     Input("table", "sorting_settings"), 
#     Input("selected-rows", "data")
#    ],
#)
#def update_graph(sorting_settings, rows):
#    _df = pd.read_json(rows["selected_rows"])
#    if sorting_settings is not None and len(sorting_settings):
#        for setting in sorting_settings:
#            _df.sort_values(
#                by=setting["column_id"],
#                ascending=(setting["direction"] == "asc"),
#                inplace=True,
#            )
#
#        return _df.to_dict("rows")
#
#    else:
#        return _df.to_dict("rows")
#

if __name__ == "__main__":
    app.run_server(debug = True)



#                    dcc.Graph(id='profit-loss',
#                              figure = {
#                                   'data':[
#                                    {'x': df_strategy['Date'], 'y': df_strategy['pnl_list'],'type': 'line', 'name':'profit'}
#                                          ]  
#                                       }
#                              )
#                        ],style = {'display':'inline-block'}
#                    )

















