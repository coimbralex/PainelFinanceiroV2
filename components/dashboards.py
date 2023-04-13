
from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from globals import *
from app import app

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
    
}

graph_margin = dict(l=25, r=25, t=25, b=0)

# =========  Layout  =========== #
layout = dbc.Col([
        dbc.Row([
                dbc.Col([
                        dbc.CardGroup([
                                dbc.Card([
                                        html.Legend('Saldo'),
                                        html.H5('R$ 1000', id='p-saldo-dashboards', style={})
                                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                                dbc.Card(
                                        html.Div(className='fa fa-university', style=card_icon),
                                        color='warning',
                                        style={'maxWidth': 75, 'height':100, 'margin-left': '-10px'}
                                )
                        ])
                ],width=4),

                #Receita
                dbc.Col([
                        dbc.CardGroup([
                                dbc.Card([
                                        html.Legend('Receita'),
                                        html.H5('R$ 10000', id='p-receita-dashboards', style={})
                                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                                dbc.Card(
                                        html.Div(className='fa fa-smile-o', style=card_icon),
                                        color='success',
                                        style={'maxWidth': 75, 'height':100, 'margin-left': '-10px'}
                                )
                        ])
                ],width=4),
                #Despesa
                dbc.Col([
                        dbc.CardGroup([
                                dbc.Card([
                                        html.Legend('Despesa'),
                                        html.H5('R$ 4600', id='p-despesa-dashboards', style={})
                                ], style={'padding-left': '20px', 'padding-top': '10px'}),
                                dbc.Card(
                                        html.Div(className='fa fa-meh-o', style=card_icon),
                                        color='warning',
                                        style={'maxWidth': 75, 'height':100, 'margin-left': '-10px'}
                                )
                        ])
                ],width=4)
        ], style={'margin':'10px'}),

        dbc.Row([
                dbc.Col([
                        dbc.Card([
                                html.Legend("Filtrar lançamentos", className="card-title"),
                                html.Label("Categorias das receitas"),
                                html.Div(
                                        dcc.Dropdown(
                                        id="dropdown-receita",
                                        clearable=False,
                                        style={"width": "100%"},
                                        persistence=True,
                                        persistence_type="session",
                                        multi=True)
                                ),

                                html.Label("Categorias das despesas"),
                                html.Div(
                                        dcc.Dropdown(
                                        id="dropdown-despesa",
                                        clearable=False,
                                        style={"width": "100%"},
                                        persistence=True,
                                        persistence_type="session",
                                        multi=True)
                                ),

                                html.Legend("Período de Análise", style={"margin-top": "10px"}),
                                dcc.DatePickerRange(
                                        month_format='Do MMM, YY',
                                        end_date_placeholder_text='Data...',
                                        start_date=datetime(2022, 4,1).date(),
                                        end_date=datetime.today()+ timedelta(days=31),
                                        updatemode='singledate',
                                        id='date-picker-config',
                                        style={'z-index': '100'}),
                                

                        ],style={'height': "100%", 'padding': '20px'})
                ], width=4),

                dbc.Col(
                        dbc.Card(dcc.Graph(id='graph1'), style={'height': '100%', 'padding': '10px'}), width=8
                )
        ], style={'margin': '10px'}),
        dbc.Row([
                dbc.Col(dbc.Card(dcc.Graph(id='graph2'), style={'padding': '10px'}), width=6),
                dbc.Col(dbc.Card(dcc.Graph(id='graph3'), style={'padding': '10px'}), width=3),
                dbc.Col(dbc.Card(dcc.Graph(id='graph4'), style={'padding': '10px'}), width=3),
        ])
])                
     

# =========  Callbacks  =========== #

#FiltroReceita
@app.callback(
        
        [Output("dropdown-receita", "options"),
        Output("dropdown-receita", "value"),
        Output("p-receita-dashboards", "children")],

        Input("store-receita","data"))

def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    val = df.Categoria.unique().tolist()

    return ([{"label": x, "value": x} for x in val], val, f"R$ {valor}")
    

#FiltroDespesa
@app.callback(
        
        [Output("dropdown-despesa", "options"),
        Output("dropdown-despesa", "value"),
        Output("p-despesa-dashboards", "children")],

        Input("store-despesa","data"))

def populate_dropdownvalues(data):
        df = pd.DataFrame(data)
        valor = df['Valor'].sum()
        val = df.Categoria.unique().tolist()

        return ([{"label": x, "value": x} for x in val], val, f"R$ {valor}") 

#Atualiza Saldo
@app.callback(

        Output("p-saldo-dashboards", "children"),

        [Input("store-despesa", "data"),
         Input("store-receita", "data")])

def saldo_total(despesa, receita):

        df_despesa = pd.DataFrame(despesa)
        df_receita = pd.DataFrame(receita)

        valor = df_receita['Valor'].sum() - df_despesa['Valor'].sum()

        return f"R$ {valor}"

#Gráfico
@app.callback(
        
        Output("graph1", "figure"),

        [Input('store-despesa', 'data'),
         Input('store-receita', 'data'),
         Input("dropdown-despesa", "value"),
         Input("dropdown-receita", "value",)]
)
def update_output(data_despesa, data_receita, despesa, receita):
       
       df_despesa = pd.DataFrame(data_despesa).set_index("Data")[["Valor"]]
       df_ds = df_despesa.groupby("Data").sum().rename(columns={"Valor": "Despesa"})

       df_receita = pd.DataFrame(data_receita).set_index("Data")[["Valor"]]
       df_rc = df_receita.groupby("Data").sum().rename(columns={"Valor": "Receita"})

       df_acum = df_ds.join(df_rc, how="outer").fillna(0)
       df_acum["Acum"] = df_acum["Receita"] - df_acum ["Despesa"]
       df_acum["Acum"] = df_acum["Acum"].cumsum()

       fig = go.Figure()
       fig.add_trace(go.Scatter(name="Fluxo de caixa", x=df_acum.index, y=df_acum["Acum"], mode="lines"))
       
       fig.update_layout(margin=graph_margin, height = 400)

#  fig.update_layout(paper_bgcolor='rgba(0,0,0,)', plot_bgcolor='rgba(0,0,0,0)')

       return fig.to_dict()

@app.callback(
       Output('graph2', 'figure'),
       
       [Input('store-receita', 'data'),
        Input('store-despesa', 'data'),
        Input('dropdown-receita', 'value'),
        Input('dropdown-despesa', 'value'),
        Input('date-picker-config', 'start_date'),
        Input('date-picker-config', 'end_date'), ]
)