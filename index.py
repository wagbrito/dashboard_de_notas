import gspread
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import dash
from app import *
 
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template

#autenticação
gc = gspread.oauth()

#abre a planilha
sh = gc.open("notas")

# Converte a planilha para um dataframe pandas
pagina = sh.worksheet('prof1')
df = pd.DataFrame(pagina.get_all_records())
df_tutor = df['Tutor'].value_counts().index 

#=== Layout ===#
app.layout = dbc.Container(children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.H2('PEI Paula Santos', style={'font-family':'Verdana', 'font-size':'60px'}),
                        html.Hr(),
                        html.P('Dashboard para acompanhar as notas dos alunos'),

                        html.H5('Tutor(a)', style={'margin-top':'20px'}),
                        dcc.Dropdown(df_tutor.sort_values(), id='drop_tutor', placeholder='Selecione tutor(a)'),
                        html.Hr(),
                        html.H5('Tutorado(a)', style={'margin-top':'20px'}),
                        dcc.Dropdown(id='drop_aluno', options=[], placeholder='Selecione aluno(a)'),
                    ]),
                ], md=3),

                dbc.Col([
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='grafico_humanas', figure=go.Figure()), lg=4, sm=12),
                        dbc.Col(dcc.Graph(id='grafico_linguagens', figure=go.Figure()), lg=4, sm=12),
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='grafico_exatas', figure=go.Figure()), lg=4, sm=12),
                        dbc.Col(dcc.Graph(id='grafico_diversificadas', figure=go.Figure()), lg=4, sm=12),
                    ])
                ]),
            ]),
], style={'padding':'10px'}, fluid=True)

#=== Callbacks ===#
#Esse primeiro callback faz o filtro dos dropdowns. Você seleciona o tutor no primeiro dropdown e o segundo mostra apenas os tutorados
@app.callback(
    Output('drop_aluno', 'options'),
    Input('drop_tutor', 'value'),
    prevent_initial_call=True
)
def update_output(value):
    df_aluno = df[df['Tutor'] == value]['Aluno']
    return df_aluno

#Esse segundo callback faz o gráfico com as disciplinas de Humanas, baseado no filtro gerado no primeiro callback
@app.callback(
    Output('grafico_humanas', 'figure'),
    Input('drop_aluno', 'value')
)
def atualiza_grafico_notas(aluno):
    notas_df = df.loc[df['Aluno'] == aluno, ['Geo1', 'His1']]
    notas = notas_df.values.tolist()[0]
    disciplinas = ['Geografia', 'História']

    fig_notas = go.Figure(data=[go.Bar(x=disciplinas, y=notas)])
    fig_notas.update_layout(yaxis_title="Nota")
    return fig_notas

#Esse terceiro callback faz o gráfico com as disciplinas de Linguagens, baseado no filtro gerado no primeiro callback
@app.callback(
    Output('grafico_linguagens', 'figure'),
    Input('drop_aluno', 'value')
)
def atualiza_grafico_notas(aluno):
    notas_df = df.loc[df['Aluno'] == aluno, ['Por1', 'Ing1', 'EF1', 'Art1']]
    notas = notas_df.values.tolist()[0]
    disciplinas = ['Português', 'Inglês', 'Educação Física', 'Arte']

    fig_notas = go.Figure(data=[go.Bar(x=disciplinas, y=notas)])
    fig_notas.update_layout(yaxis_title="Nota")
    return fig_notas

#Esse quarto callback faz o gráfico com as disciplinas de Exatas, baseado no filtro gerado no primeiro callback
@app.callback(
    Output('grafico_exatas', 'figure'),
    Input('drop_aluno', 'value')
)
def atualiza_grafico_notas(aluno):
    notas_df = df.loc[df['Aluno'] == aluno, ['Mat1', 'Cie1']]
    notas = notas_df.values.tolist()[0]
    disciplinas = ['Matemática', 'Ciência']

    fig_notas = go.Figure(data=[go.Bar(x=disciplinas, y=notas)])
    fig_notas.update_layout(yaxis_title="Nota")
    return fig_notas

#Esse quinto callback faz o gráfico com as disciplinas de Diversificadas, baseado no filtro gerado no primeiro callback
@app.callback(
    Output('grafico_diversificadas', 'figure'),
    Input('drop_aluno', 'value')
)
def atualiza_grafico_notas(aluno):
    notas_df = df.loc[df['Aluno'] == aluno, ['Pe1', 'Pv1', 'Pj1', 'Oe1', 'Tec1']]
    notas = notas_df.values.tolist()[0]
    disciplinas = ['Práticas Experimentais', 'Projeto de Vida', 'Protagonismo Juvenil', 'Orientação de Estudos', 'Tecnologia']

    fig_notas = go.Figure(data=[go.Bar(x=disciplinas, y=notas)])
    fig_notas.update_layout(yaxis_title="Nota")
    return fig_notas

#=== Run server ===#
if __name__ == "__main__":
    app.run_server(port=8050, host='127.0.0.1', debug=True)