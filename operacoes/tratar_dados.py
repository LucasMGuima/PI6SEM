from tools.filtros import Filtros
import avaliar as av
from ordenar_data import ordenar_porData

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

# Arquivo de saida dos dados
out_file = './dados_tratados/dados.csv'

# Se ele existir, pega, se não cria
if(os.path.exists(out_file)):
    df_out = pd.read_csv(out_file)
else:
    _df = pd.DataFrame(columns=['Cidade','Estado','Temp Max','Temp Min','Umidade','Umidade Min','Dia','Qualidade UR','Temp Med'])
    _df.to_csv(out_file)
    df_out = pd.read_csv(out_file, header=0)

#Pega o nome de todos os arquivos na pasta dados
path = "./dados"
dir_list = os.listdir(path)

#Abre esses arquivos com DataFrames do pandas e armazena no array dados
dados = {}
for file_name in dir_list:
    file_path = path + "//" + file_name

    data = file_name.split('.')[0].replace('_', '/')
    print(f"- {data} ")
    # Pula os dias já lidos
    if(os.path.exists(out_file) and data not in df_out['Dia'].values):
        dados[data] = pd.read_csv(file_path)
        print(f"adicionada ao csv\n")
    else: print(f"já no csv\n")

#Limpa os dados de caracteres especiais de compos especificos
tabelas = []
for  data, tabela in dados.items():
    tabela['Dia'] = data
    tabela['Qualidade UR'] = 0
    tabela['Estado'] = tabela['Estado'].apply(trim_string)
    tabela['Temp Max'] = tabela['Temp Max'].apply(remove_caracteres)
    tabela['Temp Min'] = tabela['Temp Min'].apply(remove_caracteres)
    tabela['Temp Med'] = 0
    tabela['Umidade'] = tabela['Umidade'].apply(remove_caracteres)
    tabela['Umidade Min'] = tabela['Umidade Min'].apply(remove_caracteres)

    for id, row in tabela.iterrows():
        tabela.loc[id] = av.avaliar_ur(row)
        tabela.loc[id] = av.calc_tempMedia(row)


    tabelas.append(tabela)

df: pd.DataFrame = pd.concat(tabelas, ignore_index=True)

#Ordena por data
df = ordenar_porData(df)

if(os.path.exists(out_file)):
    # Se o arquivo existe, apenas adiciona os novos valores
    df.to_csv(out_file, mode='a', header=False)
else:
    # Se não cria
    df.to_csv(out_file)