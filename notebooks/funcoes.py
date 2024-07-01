from pathlib import Path
import pandas as pd


def ler_arquivo_csv(nome_arquivo, sep=',', encoding='latin-1'):

    caminho_notebook = Path(__file__).parent
    caminho_relativo_csv = f'./data/{nome_arquivo}.csv'
    caminho_raiz = caminho_notebook.parent
    caminho_abs_csv = caminho_raiz / caminho_relativo_csv

    try:
        df = pd.read_csv(caminho_abs_csv, sep=sep,
                         encoding=encoding, low_memory=False)
        return df
    except FileNotFoundError:
        print(f"O arquivo CSV não foi encontrado em {caminho_abs_csv}")


def apresentam_sintoma(dataframe, coluna_sintoma, coluna_grupo):
    filter = dataframe[coluna_sintoma] == 1.0
    total = dataframe[coluna_grupo].shape[0]
    df_sintoma = dataframe[filter]
    lista_resultado = []

    if coluna_grupo == 'NU_IDADE_N':
        filter_criancas = dataframe[coluna_grupo] < 12
        filter_adolescentes = (dataframe[coluna_grupo] > 12) & (
            dataframe[coluna_grupo] < 18)
        filter_adultos = (dataframe[coluna_grupo] >= 18) & (
            dataframe[coluna_grupo] < 60)
        filter_idosos = dataframe[coluna_grupo] >= 60

        total_crianca = filter_criancas.sum()
        total_adolescente = filter_adolescentes.sum()
        total_adultos = filter_adultos.sum()
        total_idosos = filter_idosos.sum()

        porcentagem_crianca = (total_crianca / total * 100).round(2)
        porcentagem_adolescente = (
            total_adolescente / total * 100).round(2)
        porcentagem_adulto = (total_adultos / total * 100).round(2)
        porcentagem_idoso = (total_idosos / total * 100).round(2)

        print(f'\n{porcentagem_crianca}% dos que apresentaram sintoma de {
              coluna_sintoma} eram crianca')
        print(f'{porcentagem_adolescente}% dos que apresentaram sintoma de {
              coluna_sintoma} eram adoslecente')
        print(f'{porcentagem_adulto}% dos que apresentaram sintoma de {
              coluna_sintoma} eram adultos')
        print(f'{porcentagem_idoso}% dos que apresentaram sintoma de {
              coluna_sintoma} eram adultos')

        return [porcentagem_crianca, porcentagem_adolescente, porcentagem_adulto, porcentagem_idoso]

    else:

        par_chave_valor = dict()

        for valor in dataframe[coluna_grupo].unique():

            filter_valor = df_sintoma[coluna_grupo] == valor
            count_valor = filter_valor.sum()
            porcentagem = (count_valor / total * 100).round(2)
            print(f'{valor}: {porcentagem} %')
            par_chave_valor[str(valor)] = float(porcentagem)
        return par_chave_valor


def total_com_todos_sintomas_por_estado(dataframe, coluna_estado):

    lista_sintomas = ['FEBRE', 'TOSSE', 'GARGANTA']

    dataframe['SINTOMA'] = dataframe[lista_sintomas].isin([1]).all(axis=1)
    total_por_estado = dataframe[dataframe['SINTOMA']].groupby(
        coluna_estado).size().reset_index(name='TODOS_SINTOMAS')

    return total_por_estado


def total_com_alguns_sintomas_por_estado(dataframe, coluna_estado):

    lista_sintomas = ['FEBRE', 'TOSSE', 'GARGANTA']

    dataframe['TODOS_SINTOMAS'] = dataframe[lista_sintomas].all(axis=1)

    total_por_estado = dataframe[dataframe['TODOS_SINTOMAS']].groupby(
        coluna_estado).size().reset_index(name='TODOS_SINTOMAS')

    return total_por_estado


def grupo_risco_por_estado(df, uf):
    df_comorbidade = pd.DataFrame(index=[1.0, 2.0, 9.0])

    filter_sp = df[['SG_UF_NOT', 'DISPNEIA', 'OBESIDADE',
                    'DIABETES',	'PNEUMOPATI', 'IMUNODEPRE']]['SG_UF_NOT'] == uf
    filter_com = df.loc[filter_sp, ['DISPNEIA',
                                    'OBESIDADE',	'DIABETES',	'PNEUMOPATI', 'IMUNODEPRE']]
    for comorbidade in filter_com.columns:
        # print(filter_com[comorbidade].value_counts())
        df_comorbidade[comorbidade] = filter_com[comorbidade].value_counts()
    return df_comorbidade


def retornar_lista_uf(df):
    return df['UF']


if __name__ == '__main__':

    df = ler_arquivo_csv('populacao_2022')
    print(df.info())

    apresentam_sintoma(df, 'FEBRE', 'NU_IDADE_N')
