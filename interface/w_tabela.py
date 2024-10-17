from interface.ref import Label, Tag, Meses

import dearpygui.dearpygui as dpg
import interface.my_window as my_window, fichario as f

class WindowTabela(my_window.myWindow):
    def __init__(self, fichario: f.Fichario) -> None:
        self.fichario = fichario
        
        self._rowNumber = 100
        self.calendario = Meses()

    def criar_janela(self) -> None:
        """
            Cria a janela que mostra os dados de maneira tabular.
            Por padrão a janela mostra apenas as 100 primeiras entradas.
        """
        with dpg.window(label=Label.WindowDados,
                    tag=Tag.WindowDados,
                    width=600,
                    height=500,
                    on_close= lambda: dpg.delete_item(Tag.WindowDados)):
            #Cria a tool/menubar
            with dpg.menu_bar():
                with dpg.menu(label=Label.MenuFiltros):
                    dpg.add_menu_item(label=Label.MenuFiltroEstado, callback=self._callback_filtroEstado)
                    dpg.add_menu_item(label=Label.MenuFiltroCidade, callback=self._callback_filtroCidade)
                    dpg.add_menu_item(label=Label.MenuFiltroData, callback=self._callback_filtroData)
                dpg.add_menu_item(label=Label.MenuLimparFiltros, callback=self._callback_limparFiltros)
            #Criar tabela
            self._creat_table()
            
    def _refresh_table(self) -> None:
        dpg.delete_item(Tag.TabelaDados)
        self._creat_table()

    def _creat_table(self) -> None:
        #Cria a tabela
        with dpg.table(parent=Tag.WindowDados,
                        tag=Tag.TabelaDados,
                        header_row=True,
                        row_background=True,
                        borders_innerH=True, 
                        borders_outerH=True, 
                        borders_innerV=True,
                        borders_outerV=True):
            temp_dados = self.fichario.get_dados()
            nome_colunas = list(temp_dados)
            #Cria o cabecalho
            for nome in nome_colunas:
                    dpg.add_table_column(label=nome)

            #Adiciona as linhas da tabela
            count = 0
            for index in temp_dados.index:
                count += 1
                if count > self._rowNumber: return

                with dpg.table_row():
                    for nome in nome_colunas:
                        dpg.add_text(temp_dados.loc[index][nome])

    # ----LIMPA FILTRO----
    def _callback_limparFiltros(self) -> None:
        self.fichario.limpar_filtros()
        self._refresh_table()

    # ----FILTRO ESTADO----
    def _callback_filtroEstado(self) -> None:
        #   Cria o PopUp para a escolha de estado e chama quem aplica o filtro.
        with dpg.window(label=Label.MenuFiltroEstado, 
                        modal=True, popup=True, 
                        tag=Tag.PopupFiltroEstado,
                        on_close= lambda: dpg.delete_item(Tag.PopupFiltroEstado),
                        width=300, 
                        pos=dpg.get_item_pos(Tag.WindowDados)):
            with dpg.group(horizontal=True):
                dpg.add_text(Label.InpTextEstado)
                estados = self.fichario.get_columnEntries('Estado')
                dpg.add_combo(tag=Tag.ComboboxEstado,items=estados)
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label=Label.BtnFiltrar, callback= self._aplicar_filtroEstado)
                dpg.add_button(label=Label.BtnCancelar, callback= lambda: dpg.delete_item(Tag.PopupFiltroEstado))

    def _aplicar_filtroEstado(self) -> None:
        #   Aplica o filtro de estado se tudo ocorrer corretamente.
        estado = dpg.get_value(Tag.ComboboxEstado)
        dpg.delete_item(Tag.PopupFiltroEstado)
        self._refresh_table() if self.fichario.filtrar_estado(estado) else print("Erro ao aplicar o filtro por estado")

    # ----FILTRO CIDADE----
    def _callback_filtroCidade(self) -> None:
        #   Cria o PopUp para entrar com o nome da cidade e chama quem aplica o filtro.
        with dpg.window(label=Label.MenuFiltroCidade, 
                        modal=True, popup=True, 
                        tag=Tag.PopupFiltroCidade,
                        on_close= lambda: dpg.delete_item(Tag.PopupFiltroCidade),
                        width=300, 
                        pos=dpg.get_item_pos(Tag.WindowDados)):
            with dpg.group(horizontal=True):
                dpg.add_text(Label.InpTextCidade)    
                dpg.add_input_text(tag=Tag.InpCidade)
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label=Label.BtnFiltrar, callback= self._aplicar_filtroCidade)
                dpg.add_button(label=Label.BtnCancelar, callback= lambda: dpg.delete_item(Tag.PopupFiltroCidade))
    
    def _aplicar_filtroCidade(self) -> None:
        #   Aplica o filtro de cidade se tudo ocorrer corretamente.
        cidade = dpg.get_value(Tag.InpCidade)
        dpg.delete_item(Tag.PopupFiltroCidade)
        self._refresh_table() if self.fichario.filtrar_cidade(cidade) else print("Erro ao aplicar o filtro por cidade")

    # ----FILTRO DATA----
    def _callback_filtroData(self) -> None:
        #   Cria o PopUp para entrar com a data e chama quem aplica o filtro.
        with dpg.window(label=Label.MenuFiltroData, 
                        modal=True, popup=True, 
                        tag=Tag.PopupFiltroData,
                        on_close= lambda: dpg.delete_item(Tag.PopupFiltroData),
                        width=300, 
                        pos=dpg.get_item_pos(Tag.WindowDados)):
            with dpg.group():
                with dpg.group(horizontal=True):
                    dpg.add_text(Label.InpTextDia) 
                    dias_inTable = self.fichario.get_columnEntries('Dia')
                    dias = []
                    for el in dias_inTable:
                        dia = str(el).split('/')[0]
                        if dia not in dias: dias.append(int(dia)) 
                    dias.sort()
                    dpg.add_combo(tag=Tag.ComboboxDia,items=dias)

                with dpg.group(horizontal=True):
                    dpg.add_text(Label.InpTextMes)
                    meses_inTable = self.fichario.get_columnEntries('Dia')
                    lst_nomeMeses = []
                    for el in meses_inTable:
                        mes_num = str(el).split('/')[1]
                        mes_nome = self.calendario.get_mesNome(int(mes_num))
                        if mes_nome not in lst_nomeMeses: lst_nomeMeses.append(mes_nome) 
                    dpg.add_combo(tag=Tag.ComboboxMes,items=lst_nomeMeses)
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label=Label.BtnFiltrar, callback= self._aplicar_filtroData)
                dpg.add_button(label=Label.BtnCancelar, callback= lambda: dpg.delete_item(Tag.PopupFiltroData))
        pass

    def _aplicar_filtroData(self) -> None:
        #   Aplica o filtro de cidade se tudo ocorrer corretamente.
        dia = dpg.get_value(Tag.ComboboxDia)
        mes = dpg.get_value(Tag.ComboboxMes)

        dpg.delete_item(Tag.PopupFiltroData)

        mes = self.calendario.get_mesNumber(mes)

        data = f"{dia}/{mes}/2024"

        self._refresh_table() if self.fichario.filtrar_dia(data) else print("Erro ao aplicar o filtro por data")