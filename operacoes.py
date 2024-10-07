import fichario as f
import pandas as pd

import os


def run_coleta() -> f.Fichario:
    """
        Operação de coleta de dados, coleta os dados do dia atual

        Return
        -------
        Retorna um ficharia com os dados atualizados
    """
    os.system("python .\operacoes\coletar_dados.py")
    os.system("python .\operacoes\\tratar_dados.py")

    return f.Fichario(pd.read_csv('./dados_tratados/dados.csv', index_col=0))

def calc_tempMedia(fichario: f.Fichario) -> int:
    """
        Calcula a media das temperaturas.

        Parameters
        ----
        fichario: f.Fichario
            Fichario com os dados a serem usados
        
        Return
        -------
        A temperatura média
    """
    col_tempMedia = fichario.get_columnEntries('Temp Med', agrupar=False)
    tempMedia = 0
    for temp in col_tempMedia:
        tempMedia += temp
    tempMedia /= len(col_tempMedia)

    return int(tempMedia)


def calc_umiMedia(fichario: f.Fichario) -> int:
    """
        Calcula a media da umidade.

        Parameters
        ----
        fichario: f.Fichario
            Fichario com os dados a serem usados
        
        Return
        -------
        A umidade média
    """
    col_umi = fichario.get_columnEntries('Umidade', agrupar=False)
    umiMedia = 0
    for umi in col_umi:
        umiMedia += umi
    umiMedia /= len(col_umi)
    
    return int(umiMedia)

def calc_ampliTemp(fichario: f.Fichario) -> int:
    col_tempMax = fichario.get_columnEntries('Temp Max')
    col_tempMin = fichario.get_columnEntries('Temp Min')

    tempMax = max(col_tempMax)
    tempMin = min(col_tempMin)

    ampli = tempMax - tempMin
    return ampli