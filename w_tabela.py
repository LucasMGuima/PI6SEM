from ref import Label, Tag

import dearpygui.dearpygui as dpg
import pandas as pd

import my_window, fichario as f


from datetime import datetime


class WindowTabela(my_window.myWindow):
    def __init__(self, fichario: f.Fichario) -> None:
        self.fichario = fichario
        self._rowNumber = 100

    def criar_janela(self) -> None:
        """
            Cria a janela que mostra os dados de maneira tabular.
            Por padrão a janela mostra apenas as 100 primeiras entradas.
        """
        with dpg.window(label=Label.WindowDados,
                    tag=Tag.WindowDados,
                    width=600,
                    height=500,
                    on_close=super().close_window):
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
                    dpg.add_table_column(label=nome, tag=nome)

            #Adiciona as linhas da tabela
            count = 0
            for index in temp_dados.index:
                count += 1
                if count > self._rowNumber: return
                
                with dpg.table_row():
                    for nome in nome_colunas:
                        print(temp_dados)
                        dpg.add_text(temp_dados.iloc[index][nome])

    def _callback_limparFiltros(self) -> None:
        self.fichario.limpar_filtros()
        self._refresh_table()

    def _callback_filtroEstado(self) -> None:
        with dpg.window(label=Label.MenuFiltroEstado, 
                        modal=True, popup=True, 
                        tag=Tag.PopupFiltroEstado, 
                        width=300, 
                        pos=dpg.get_item_pos(Tag.WindowDados)):
            with dpg.group(horizontal=True):
                dpg.add_text(label=Label.InpTextEstado)
                estados = self.fichario.get_columnEntries('Estado')
                dpg.add_combo(tag=Tag.ComboboxEstado,items=estados)
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label=Label.BtnFiltrar, callback= self._aplicar_filtroEstado)
                dpg.add_button(label=Label.BtnCancelar, callback= lambda: dpg.delete_item(Tag.PopupFiltroEstado))

    def _aplicar_filtroEstado(self) -> None:
        estado = dpg.get_value(Tag.ComboboxEstado)
        dpg.delete_item(Tag.PopupFiltroEstado)
        self._refresh_table() if self.fichario.filtrar_estado(estado) else print("Erro ao aplicar o filtro por estado")

    def _callback_filtroCidade(self) -> None:
        with dpg.window(label=Label.MenuFiltroCidade, 
                        modal=True, popup=True, 
                        tag=Tag.PopupFiltroCidade, 
                        width=300, 
                        pos=dpg.get_item_pos(Tag.WindowDados)):
            with dpg.group(horizontal=True):
                dpg.add_text(label=Label.InpTextCidade)    
                dpg.add_input_text(tag=Tag.InpCidade)
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_button(label=Label.BtnFiltrar, callback= self._aplicar_filtroCidade)
                dpg.add_button(label=Label.BtnCancelar, callback= lambda: dpg.delete_item(Tag.PopupFiltroCidade))
    
    def _aplicar_filtroCidade(self) -> None:
        cidade = dpg.get_value(Tag.InpCidade)
        print(cidade)
        self._refresh_table() if self.fichario.filtrar_cidade(cidade) else print("Erro ao aplicar o filtro por cidade")

    def _callback_filtroData(self) -> None:
        self._refresh_table() if self.fichario.filtrar_dia('20/8/2024') else print("Erro ao aplicar o filtro por data")