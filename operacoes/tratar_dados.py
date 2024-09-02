from tools.filtros import Filtros

import pandas as pd
import os, re

def trim_string(value: str) -> str:
    """
        Remove espaços em branco do começo e final da string.
        Se não conseguir retorna a string inicial.
    """
    try:
        return value.strip()
    except:
        return value

def remove_caracteres(value: str) -> int:
    """
        Usa RegEx para pegar apenas a parte numerica do valor, e retornalo como um inteiro
    """
    try:
        temp = re.search("\d+", value)
        return int(temp.group())
    except:
        return 0
    
filtrar = Filtros()

#Pega o nome de todos os arquivos na pasta dados
path = "./dados"
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
    tabela['Estado'] = tabela['Estado'].apply(trim_string)
    tabela['Temp Max'] = tabela['Temp Max'].apply(remove_caracteres)
    tabela['Temp Min'] = tabela['Temp Min'].apply(remove_caracteres)
    tabela['Umidade'] = tabela['Umidade'].apply(remove_caracteres)
    tabela['Umidade Min'] = tabela['Umidade Min'].apply(remove_caracteres)

    tabelas.append(tabela)


df: pd.DataFrame = pd.concat(tabelas, ignore_index=True)

df.to_csv('./dados_tratados/dados.csv')