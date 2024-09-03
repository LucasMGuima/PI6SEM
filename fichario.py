from operacoes.tools.filtros import Filtros
import pandas as pd

class Fichario():
    """
        Classe que controla a atual situação dos dados
    """
    def __init__(self, dados: pd.DataFrame):
        """
            Inicia uma instancia da classe Fichario

            Parametros:\n
            **dados** -> Pandas DataFrame contendo os dados iniciais.
        """
        self._dados_originais: pd.DataFrame = dados
        self._dados: pd.DataFrame = self._dados_originais
        self.filtros = Filtros()

    def get_dados(self) -> pd.DataFrame:
        """
            Retorna os dados contidos no fichario
        """
        return self._dados

    def get_columnEntries(self, column_name: str, agrupar: bool = True) -> list:
        """
            Pega as entradas de uma coluna em especifico. Por pradão agrupa todos os dados iguais

            Parametros:\n
            **column_name** -> String do nome da coluna,\n
            **agrupar** (default: True)-> Boolena, Indica se é para voltar todos os dados, ou agrupar as repetições.
       
            Return:\n
            Retrona uma lista contendo os dados encontrados na coluna        
        """

        return list(self._dados[column_name].drop_duplicates()) if agrupar else list(self._dados[column_name])

    def limpar_filtros(self) -> None:
        """
            Limpa os filtros aplicados aos dados. 
        """
        self._dados = self._dados_originais

    def filtrar_estado(self, estado: str) -> bool:
        """
            Filtra os dados com base no estado escolhido.
            Salva os dados filtrados na variavel dados.

            Parametros:\n
            **estado** -> sigla do estado escolhido

            Retorno:\n
            **False** -> se algo deu errado, não aplica o filtro\n
            **True** -> se tudo ocorreu como esperado
        """
        if len(estado) > 2:
            return False
        
        temp_dados = self.filtros.estado(estado, self._dados)
        if temp_dados.size <= 0:
            return False
        self._dados = temp_dados
        return True
    
    def filtrar_cidade(self, cidade: str) -> bool:
        """
            Filtra os dados com base na cidade escolhida.
            Salva os dados filtrados na variavel dados.

            Parametros:\n
            **cidade** -> nome da cidade escolhida.

            Retorno:\n
            **False** -> se algo deu errado, não aplica o filtro\n
            **True** -> se tudo ocorreu como esperado
        """
        temp_dados = self.filtros.cidade(cidade, self._dados)
        if temp_dados.size <= 0:
            return False
        self._dados = temp_dados
        return True
    
    def filtrar_dia(self, data: str) -> bool:
        """
            Filtra os dados com base na data escolhida.
            Salva os dados filtrados na variavel dados.

            Parametros:\n
            **data** -> data, no formato dd/mm/ano, escolhida.

            Retorno:\n
            **False** -> se algo deu errado, não aplica o filtro\n
            **True** -> se tudo ocorreu como esperado
        """

        temp_dados = self.filtros.data(data, self._dados)
        if temp_dados.size <= 0:
            return False
        self._dados = temp_dados
        return True