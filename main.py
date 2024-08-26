import pandas as pd
import os, re

def remove_caracteres(value: str) -> int:
    """
        Usa RegEx para pegar apenas a parte numerica do valor, e retornalo como um inteiro
    """
    try:
        temp = re.search("\d+", value)
        return int(temp.group())
    except:
        return 0

def filtrar_estado(estado: str, dados: dict) -> pd.DataFrame:
    """
        Filtra so dados e retorna apenas as entrados do estado especifico

        Parametros:\n
        **estado** -> string do nome do estado.\n
        **dados** -> dicionario que contem os dados, tendo o dia como chave.\n
        **Retorno**:\n
        Retorna um DataFrame do pandas com os dados do estado e o dia dos dados\n
    """

    pass

#Pega o nome de todos os arquivos na pasta dados
path = ".//dados"
dir_list = os.listdir(path)

#Abre esses arquivos com DataFrames do pandas e armazena no array dados
dados = {}
for file_name in dir_list:
    file_path = path + "//" + file_name

    data = file_name.split('.')[0].replace('_', '/')
    dados[data] = pd.read_csv(file_path)

#Limpa os dados de caracteres especiais de compos especificos
tabelas = []
for  data, tabela in dados.items():
    tabela['Dia'] = data
    tabela['Temp Max'] = tabela['Temp Max'].apply(remove_caracteres)
    tabela['Temp Min'] = tabela['Temp Min'].apply(remove_caracteres)
    tabela['Umidade'] = tabela['Umidade'].apply(remove_caracteres)
    tabela['Umidade Min'] = tabela['Umidade Min'].apply(remove_caracteres)

    tabelas.append(tabela)


df: pd.DataFrame = pd.concat(tabelas, ignore_index=True)

#print(filtrar_estado('São Paulo', df))

print(df['Cidade'].value_counts().to_csv('./qtd_entradas.csv'))