from layout.componentes import dcc, create_navbar, dbc
import plotly.express as px
from notebooks.funcoes import *

df_estados = ler_arquivo_csv('populacao')
df_dados_epidemiologicos = ler_arquivo_csv('srag_2019')
dados_todos_sintomas = total_com_todos_sintomas_por_estado(
    df_dados_epidemiologicos, 'SG_UF_NOT')
dados_alguns_sintomas = total_com_alguns_sintomas_por_estado(
    df_dados_epidemiologicos, 'SG_UF_NOT')
lista_estado = retornar_lista_uf(df_estados)


def cria_grafico_bar(df, eixo_x, eixo_y, titulo):
    fig = px.bar(df, x=eixo_x, y=eixo_y,
                 title=titulo)
    fig.update_layout(xaxis_title='Unidades Federativas',
                      yaxis_title='Número de Casos', xaxis_tickangle=-45)
    return fig


def cria_grafico_comorbidades(df, uf):
    df_comorbidade = grupo_risco_por_estado(df, uf)

    df_comorbidade = df_comorbidade.reset_index().melt(
        id_vars=['index'], var_name='Comorbidade', value_name='Contagem')
    df_comorbidade.rename(columns={'index': 'Valor'}, inplace=True)

    fig = px.bar(df_comorbidade, x='Comorbidade', y='Contagem', color='Valor', barmode='group',
                 title=f'Contagem de Comorbidades por Valor - {uf}',
                 labels={'Comorbidade': 'Comorbidade', 'Contagem': 'Contagem', 'Valor': 'Valor'})
    return fig


def create_layout():

    layout = dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    create_navbar(),
                    sm=12
                )
            ),

            dbc.Row(
                [

                    dbc.Col(
                        [
                            dcc.Graph(id='bar-chart',
                                      figure=cria_grafico_bar(dados_alguns_sintomas, 'SG_UF_NOT', 'TODOS_SINTOMAS', 'Total de Pacientes com pelo menos 1 Sintoma')),

                        ], sm=6
                    ),

                    dbc.Col(
                        [
                            dcc.Graph(id='bar-chart',
                                      figure=cria_grafico_bar(dados_todos_sintomas, 'SG_UF_NOT', 'TODOS_SINTOMAS', 'Total de Pacientes com Todos os Sintomas'))

                        ], sm=6
                    )
                ]
            ),
            dbc.Row(
                dbc.Col(
                    create_navbar(),
                    sm=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    dcc.Dropdown(
                        id='dropdown-uf',
                        options=[{'label': uf, 'value': uf}
                                 for uf in lista_estado],
                        value='uf',
                    ),
                    width=4,
                ),
                align="center",
                className="my-4"
            ),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(
                        id='bar-chart'
                    ),
                )
            )
        ], fluid=True
    )

    return layout


def callback_dropdown_estados(app):
    from dash.dependencies import Input, Output

    @app.callback(
        Output('bar-chart', 'figure'),
        Input('dropdown-uf', 'value')
    )
    def cria_grafico_comorbidades(uf):
        df_comorbidade = grupo_risco_por_estado(df_dados_epidemiologicos, uf)

        df_comorbidade = df_comorbidade.reset_index().melt(
            id_vars=['index'], var_name='Comorbidade', value_name='Contagem')
        df_comorbidade.rename(columns={'index': 'Valor'}, inplace=True)

        valor_labels = {
            1.0: 'Sim',
            2.0: 'Não',
            9.0: 'Ignorado'
        }

        df_comorbidade['Valor'] = df_comorbidade['Valor'].map(valor_labels)

        fig = px.bar(df_comorbidade, x='Comorbidade', y='Contagem', color='Valor', barmode='group',
                     title=f'Contagem de Comorbidades por Valor - {uf}',
                     labels={'Comorbidade': 'Comorbidade',
                             'Contagem': 'Contagem', 'Valor': 'Valor'},
                     category_orders={'Valor': ['Sim', 'Não', 'Ignorado']})
        return fig
