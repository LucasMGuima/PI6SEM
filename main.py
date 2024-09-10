import pandas as pd
import dearpygui.dearpygui as dpg
import os, threading, w_tabela, w_temperatura, fichario as f

from ref import Tag, Label
from datetime import date

# Funcoes internas
def _run_coleta():
    os.system("python .\operacoes\coletar_dados.py")
    os.system("python .\operacoes\\tratar_dados.py")
    global fichario
    fichario = f.Fichario(pd.read_csv('./dados_tratados/dados.csv', index_col=0))

# Callbacks
def callback_showTabel():
    win_tabela = w_tabela.WindowTabela(fichario)
    win_tabela.criar_janela()

def callback_coletarDados():
    thread = threading.Thread(target=_run_coleta)
    thread.start()

def callback_showTemperatura():
    p_temp = w_temperatura.WindowTemperatura(fichario)
    p_temp.criar_janela()

# Funcoes de paines
def painel_configPesquisa():
    with dpg.child_window(width=250):
        dpg.add_text("Dados de pesquisa")
        with dpg.group():
            with dpg.group(horizontal=True):
                dpg.add_text("Estado: ")
                dpg.add_combo()
            with dpg.group(horizontal=True):
                dpg.add_text("Cidade: ")
                dpg.add_combo()
            dpg.add_separator()
            dpg.add_text("Periodo")
            with dpg.group(horizontal=True):
                dpg.add_text("De: ")
                dpg.add_combo()
            with dpg.group(horizontal=True):
                dpg.add_text("Até: ")
                dpg.add_combo()
            dpg.add_button(label="Mostrar")

global fichario
fichario = f.Fichario(pd.read_csv('./dados_tratados/dados.csv', index_col=0))

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
    
    with dpg.group(horizontal=True):
        painel_configPesquisa()

        with dpg.group():
            with dpg.group(horizontal=True):
                with dpg.child_window(height=270, width=500):
                    with dpg.group(horizontal=True):
                        dpg.add_text("Score: ")
                        dpg.add_text("BOM")
                    dpg.add_plot()
                with dpg.child_window(height=270, width=200):
                    dpg.add_text("Medias/Amplitude")
        
            with dpg.child_window(height=350):
                dpg.add_plot()

    

dpg.create_viewport(title='PI6SEM', width=1000, height=700, x_pos=0, y_pos=0)
dpg.set_primary_window(Tag.WindowPrimary, True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()