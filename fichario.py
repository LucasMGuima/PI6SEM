from func.tools.filtros import Filtros
from scipy.stats import pearsonr
import pandas as pd, matplotlib.pyplot as plt

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

    def intarvalo_datas(self, data_ini: str, data_fim: str) -> bool:
        """
            Filtra os dados com base no intervalo estabelecido.

            Prametros:\n
            **data_ini** -> data inicial no foramto dd/mm/aaaa\n
            **data_fim** -> data final no foramto dd/mm/aaaa

            Retorno:\n
            **False** -> se algo deu errado, não aplica o filtro\n
            **True** -> se tudo ocorreu como esperado
        """
        try:
            dia_ini, mes_ini, ano_ini = data_ini.split('/')
            dia_fim, mes_fim, ano_fim = data_fim.split('/')

            lst_dias = self.get_columnEntries('Dia')

            tabela_intervalo = pd.DataFrame()

            for data in lst_dias:
                dia, mes, ano = str(data).split('/')

                dentro_intervalo_mes: bool = (int(mes) >= int(mes_ini) and int(mes) <= int(mes_fim))
                dentro_intervalo_dia: bool = False

                if(int(mes) == int(mes_ini)):
                    dentro_intervalo_dia: bool = int(dia) >= int(dia_ini)
                elif(int(mes) == int(mes_fim)):
                    dentro_intervalo_dia: bool = int(dia) <= int(dia_fim)
                elif(dentro_intervalo_mes):
                    dentro_intervalo_dia: bool = True

                if dentro_intervalo_dia and dentro_intervalo_mes:
                    tabela_intervalo = pd.concat([tabela_intervalo,self.get_dados().loc[self.get_dados()['Dia'] == data]], ignore_index=True)
            
            self._dados = tabela_intervalo
            return True
        except Exception as e:
            print(e)
            return False

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