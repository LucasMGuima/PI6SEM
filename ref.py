class Tag():
    WindowPrimary = 1
    TabelaDados = 2
    WindowDados = 3
    PopupFiltroEstado = 4
    ComboboxEstado = 5
    PopupFiltroCidade = 6
    InpCidade = 7
    PopupFiltroData = 8
    InpDia = 9
    ComboboxDia = 10
    InpMes = 11
    ComboboxMes = 12
    ComboEstado = 13
    ComboCidade = 14
    plotTempUmidade = 15
    plotYTempMax = 16
    plotYTempMin = 17
    plotYUmidade = 18
    plotYUmiMin = 19
    plotYAxis = 20
    piePlot = 21

class Label():
    WindowDados = 'Dados'
    WindowPrimary = 'Primary'

    MenuJanelas = 'Janelas'
    MenuItemTabela = 'Tabela'
    MenuOperacoes = 'Operações'
    MenuItemColetar = 'Coletar Dados'
    MenuFiltros = 'Filtros'
    MenuFiltroEstado = 'Filtrar por estado'
    MenuFiltroCidade = 'Filtrar por cidade'
    MenuFiltroData = 'Filtrar por data'
    MenuLimparFiltros = 'Limpar Filtros'

    InpTextEstado = "Estado: "
    InpTextCidade = "Cidade: "
    InpTextDia  = "Dia: "
    InpTextMes = "Mês"

    BtnFiltrar = "Filtrar"
    BtnCancelar = "Cancelar"

class Meses():
    meses = {
        1: 'Janeiro',
        2: 'Fevereiro',
        3: 'Março',
        4: 'Abril',
        5: 'Maio',
        6: 'Junho',
        7: 'Julho',
        8: 'Agosto',
        9: 'Setembro',
        10: 'Outubro',
        11: 'Novembro',
        12: 'Dezembro'
    }

    def get_mesNumber(self, nome: str) -> int:
        """
            Retorna o numero correspondente ao nome do mes.

            **Parametros**:\n
            **nome** -> String contendo o nome do mês.

            **Retorno**:\n
            Retorna o numero do mês ou **0 se não encontrar**
        """
        for i, v in self.meses.items():
            if v == nome:
                return i
        return 0
    
    def get_mesNome(self, numero: int) -> str:
        """
            Retorna o nome correspondente ao numero entrado.

            **Parametros**:\n
            **numero** -> Int contendo o numero do mês.

            **Retorno**:\n
            Retorna o nome do mês ou **None se não encontrar**
        """
        try:
            return self.meses[numero]
        except:
            return None
        
class UR():
    qualidade = {
        1: "Umidade Excessiva - 60% - 100%",
        2: "Confortavel 40% - 60%",
        3: "Seco 30% - 40%",
        4: "Atenção 20% - 30%",
        5: "Alerta 12% - 20%",
        6: "Emergencia Até 12%"
    }