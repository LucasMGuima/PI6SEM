import pandas as pd

class Filtros():
    """
        Classe que armazena os filtros usados.
    """
    def estado(self, estado: str, df: pd.DataFrame) -> pd.DataFrame:
        """
            Filtra so dados e retorna apenas as entradas do estado especifico

            Parametros:\n
            **estado** -> string do nome do estado.\n
            **df** -> dataframe do pandas que contem os dados.\n
            **Retorno**:\n
            Retorna um DataFrame do pandas com os dados do estado e o dia dos dados\n
        """
        return df.loc[df['Estado'] == estado]

    def cidade(self, cidade: str, df: pd.DataFrame) -> pd.DataFrame:
        """
            Filtra so dados e retorna apenas as entradas da cidade especificada

            Parametros:\n
            **cidade** -> string do nome da cidade.\n
            **df** -> dataframe do pandas que contem os dados.\n
            **Retorno**:\n
            Retorna um DataFrame do pandas com os dados do estado e o dia dos dados\n
        """
        return df.loc[df['Cidade'] == cidade]

    def data(self, data: str, df: pd.DataFrame) -> pd.DataFrame:
        """
            Filtra so dados e retorna apenas as entradas da data especifica.

            Parametros:\n
            **data** -> string da data especifica no formato dd/mm/yy.\n
            **df** -> dataframe do pandas que contem os dados.\n
            **Retorno**:\n
            Retorna um DataFrame do pandas com os dados do estado e o dia dos dados\n
        """
        return df.loc[df['Dia'] == data]