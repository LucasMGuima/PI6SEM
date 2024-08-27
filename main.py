import pandas as pd
import dearpygui.dearpygui as dpg

from ref import Tag, Label

import os, threading

dpg.create_context()

def close_window(sender):
    dpg.delete_item(sender)

def _carregar_dados() -> pd.DataFrame:
    dados: pd.DataFrame = pd.read_csv('./dados_tratados/saida.csv', index_col=0)
    return dados

def callback_showTabel():
    dados = _carregar_dados()
    with dpg.window(label=Label.WindowDados,
                    tag=Tag.WindowDados,
                    on_close=close_window):
        #Cria a tool/menubar
        with dpg.menu_bar():
            dpg.add_menu_item(label="Filtros")

        #Cria a tabela
        with dpg.table(tag=Tag.TabelaDados,
                        header_row=True, 
                        row_background=True,
                        borders_innerH=True, 
                        borders_outerH=True, 
                        borders_innerV=True,
                        borders_outerV=True):
            nome_colunas = list(dados)
            #Cria o cabecalho
            for nome in nome_colunas:
                    dpg.add_table_column(label=nome, tag=nome)

            #Adiciona as linhas da tabela
            for index in dados.index:
                with dpg.table_row():
                    for nome in nome_colunas:
                        dpg.add_text(dados[nome][index])

def _run_coleta():
    os.system("python .\operacoes\coletar_dados.py")
    os.system("python .\operacoes\\tratar_dados.py")

def callback_coletarDados():
    thread = threading.Thread(target=_run_coleta)
    thread.start()

#Janela principal
with dpg.window(tag=Tag.WindowPrimary):
    #Cria a toolbar/menubar
    with dpg.menu_bar():
        with dpg.menu(label=Label.MenuJanelas):
            dpg.add_menu_item(label=Label.MenuItemTabela, callback=callback_showTabel)
        with dpg.menu(label=Label.MenuOperacoes):
            dpg.add_menu_item(label=Label.MenuItemColetar, callback=callback_coletarDados)
                    
dpg.create_viewport(title='PI6SEM', width=600, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window(Tag.WindowPrimary, True)
dpg.start_dearpygui()
dpg.destroy_context()