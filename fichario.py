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
        self.dados: pd.DataFrame = self._dados_originais
        self.filtros = Filtros()

    def limpar_filtros(self) -> None:
        """
            Limpa os filtros aplicados aos dados. 
        """
        self.dados = self._dados_originais

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
        
        temp_dados = self.filtros.estado(estado, self.dados)
        if temp_dados.size <= 0:
            return False
        self.dados = temp_dados
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
        tepm_dados = self.filtros.cidade(cidade, self.dados)
        if tepm_dados.size <= 0:
            return False
        self.dados = tepm_dados
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

        temp_dados = self.filtros.data(data, self.dados)
        if temp_dados.size <= 0:
            return False
        self.dados = temp_dados
        return True