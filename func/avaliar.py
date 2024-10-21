import pandas as pd
import math


def avaliar_ur(row: pd.Series) -> pd.Series:
    umidade = int(row["Umidade"])
    umidade_min = int(row["Umidade Min"])

    umidade_med = (umidade_min + umidade) / 2

    if(umidade_med >= 60):
        row['Qualidade UR'] = 1
    elif(umidade_med < 60 and umidade_med >= 40):
        row['Qualidade UR'] = 2
    elif(umidade_med < 40 and umidade_med >= 30):
        row['Qualidade UR'] = 3
    elif(umidade_med < 30 and umidade_med >= 20):
        row['Qualidade UR'] = 4
    elif(umidade_med < 20 and umidade_med >= 12):
        row['Qualidade UR'] = 5
    elif(umidade_med < 12):
        row['Qualidade UR'] = 6

    return row

def calc_tempMedia(row: pd.Series) -> pd.Series:
    tempMax = int(row['Temp Max'])
    tempMin = int(row['Temp Min'])

    media = (tempMax + tempMin)/2
    media = math.floor(media)

    row['Temp Med'] = media

    return row

def rankear_cidade(fichario) -> list:
    """
        Avalia as cidades e mostra quais são as melhores para se viver com base na avaliação da umidade relativa

        **Argumentos**\n 
        ficario: f.Fichario contendo os dados a serem avaliados.

        **Retorno**\n
        Lista ordenada da melhor cidade para pior
    """

    lst_cidade: list = fichario.get_columnEntries('Cidade')
    for cidade in lst_cidade:
        pass
