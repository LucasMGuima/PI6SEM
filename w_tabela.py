from ref import Label, Tag

import dearpygui.dearpygui as dpg
import pandas as pd

import my_window, fichario as f

class WindowTabela(my_window.myWindow):
    def __init__(self, fichario: f.Fichario) -> None:
        self.fichario = fichario
        self.dados = self.fichario.dados

    def criar_janela(self) -> None:
        """
            Cria a janela que mostra os dados de maneira tabular.
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
            #Cria a tabela
            with dpg.table(tag=Tag.TabelaDados,
                        header_row=True, 
                        row_background=True,
                        borders_innerH=True, 
                        borders_outerH=True, 
                        borders_innerV=True,
                        borders_outerV=True):
                nome_colunas = list(self.dados)
                #Cria o cabecalho
                for nome in nome_colunas:
                        dpg.add_table_column(label=nome, tag=nome)

                #Adiciona as linhas da tabela
                for index in self.dados.index:
                    with dpg.table_row():
                        for nome in nome_colunas:
                            dpg.add_text(self.dados[nome][index])
        
            
    def _refresh_table(self) -> None:
        self.dados = self.fichario.dados
        dpg.delete_item(Tag.TabelaDados)
        #Cria a tabela
        with dpg.table(parent=Tag.WindowDados,
                        tag=Tag.TabelaDados,
                        header_row=True, 
                        row_background=True,
                        borders_innerH=True, 
                        borders_outerH=True, 
                        borders_innerV=True,
                        borders_outerV=True):
            nome_colunas = list(self.dados)
            #Cria o cabecalho
            for nome in nome_colunas:
                    dpg.add_table_column(label=nome, tag=nome)

            #Adiciona as linhas da tabela
            for index in self.dados.index:
                with dpg.table_row():
                    for nome in nome_colunas:
                        dpg.add_text(self.dados[nome][index])

    def _callback_limparFiltros(self) -> None:
        self.fichario.limpar_filtros()
        self._refresh_table()

    def _callback_filtroEstado(self) -> None:
        with dpg.window(label=Label.MenuFiltroEstado, modal=True, popup=True, tag=Tag.PopupFiltroEstado, width=300, pos=dpg.get_mouse_pos()):
            with dpg.group(horizontal=True):
                dpg.add_text(label=Label.InpTextEstado)
                estados = list(self.dados['Estado'].drop_duplicates())
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
        self._refresh_table() if self.fichario.filtrar_cidade('São Paulo') else print("Erro ao aplicar o filtro por cidade")

    def _callback_filtroData(self) -> None:
        self._refresh_table() if self.fichario.filtrar_dia('20/8/2024') else print("Erro ao aplicar o filtro por data")