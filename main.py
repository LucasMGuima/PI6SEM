import pandas as pd
import dearpygui.dearpygui as dpg

from ref import Tag, Label

import os, threading, w_tabela, fichario as f

def _run_coleta():
    os.system("python .\operacoes\coletar_dados.py")
    os.system("python .\operacoes\\tratar_dados.py")

def callback_showTabel():
    win_tabela = w_tabela.WindowTabela(fichario)
    win_tabela.criar_janela()

def callback_coletarDados():
    thread = threading.Thread(target=_run_coleta)
    thread.start()


fichario = f.Fichario( pd.read_csv('./dados_tratados/saida.csv', index_col=0))

dpg.create_context()

#Janela principal
with dpg.window(tag=Tag.WindowPrimary):
    #Cria a toolbar/menubar
    with dpg.menu_bar():
        with dpg.menu(label=Label.MenuJanelas):
            dpg.add_menu_item(label=Label.MenuItemTabela, callback=callback_showTabel)
        with dpg.menu(label=Label.MenuOperacoes):
            dpg.add_menu_item(label=Label.MenuItemColetar, callback=callback_coletarDados)
                    
dpg.create_viewport(title='PI6SEM', x_pos=0, y_pos=0)
dpg.setup_dearpygui()
dpg.show_viewport(maximized=True)
dpg.set_primary_window(Tag.WindowPrimary, True)
dpg.start_dearpygui()
dpg.destroy_context()