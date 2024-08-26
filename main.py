import pandas as pd
import dearpygui.dearpygui as dpg

from ref import Tag, Label

dados: pd.DataFrame = pd.read_csv('./dados_tratados/saida.csv', index_col=0)

dpg.create_context()

def close_window(sender):
    dpg.delete_item(sender)

def show_tabel():
    with dpg.window(label=Label.WindowDados,
                    tag=Tag.WindowDados,
                    on_close=close_window):
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

#Janela principal
with dpg.window(tag=Tag.WindowPrimary):
    #Cria a toolbar/menubar
    with dpg.menu_bar():
        with dpg.menu(label=Label.MenuJanelas):
            dpg.add_menu_item(label=Label.MenuItemTabela, callback=show_tabel)  
                    
dpg.create_viewport(title='PI6SEM', width=600, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window(Tag.WindowPrimary, True)
dpg.start_dearpygui()
dpg.destroy_context()