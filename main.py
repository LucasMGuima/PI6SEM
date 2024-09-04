import pandas as pd
import dearpygui.dearpygui as dpg
import os, threading, w_tabela, w_temperatura, fichario as f

from ref import Tag, Label
from datetime import date

def _run_coleta():
    os.system("python .\operacoes\coletar_dados.py")
    os.system("python .\operacoes\\tratar_dados.py")
    global fichario
    fichario = f.Fichario(pd.read_csv('./dados_tratados/dados.csv', index_col=0))

def callback_showTabel():
    win_tabela = w_tabela.WindowTabela(fichario)
    win_tabela.criar_janela()

def callback_coletarDados():
    thread = threading.Thread(target=_run_coleta)
    thread.start()

def callback_showTemperatura():
    p_temp = w_temperatura.WindowTemperatura(fichario)
    p_temp.criar_janela()

global fichario
fichario = f.Fichario( pd.read_csv('./dados_tratados/dados.csv', index_col=0))

dpg.create_context()

#Janela principal
with dpg.window(tag=Tag.WindowPrimary):
    #Cria a toolbar/menubar
    with dpg.menu_bar():
        with dpg.menu(label=Label.MenuJanelas):
            dpg.add_menu_item(label=Label.MenuItemTabela, callback=callback_showTabel)
            dpg.add_menu_item(label="Gráfico de Temperatura", callback=callback_showTemperatura)
        with dpg.menu(label=Label.MenuOperacoes):
            dpg.add_menu_item(label=Label.MenuItemColetar, callback=callback_coletarDados)

    
    

dpg.create_viewport(title='PI6SEM', x_pos=0, y_pos=0)
dpg.set_primary_window(Tag.WindowPrimary, True)
dpg.setup_dearpygui()
dpg.show_viewport(maximized=True)
dpg.start_dearpygui()
dpg.destroy_context()