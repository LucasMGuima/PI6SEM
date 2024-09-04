import pandas as pd
import dearpygui.dearpygui as dpg
import os, threading, w_tabela, fichario as f

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


global fichario
fichario = f.Fichario( pd.read_csv('./dados_tratados/dados.csv', index_col=0))

dpg.create_context()

#Janela principal
with dpg.window(tag=Tag.WindowPrimary):
    #Cria a toolbar/menubar
    with dpg.menu_bar():
        with dpg.menu(label=Label.MenuJanelas):
            dpg.add_menu_item(label=Label.MenuItemTabela, callback=callback_showTabel)
        with dpg.menu(label=Label.MenuOperacoes):
            dpg.add_menu_item(label=Label.MenuItemColetar, callback=callback_coletarDados)
    
    #Painel de plot
    fichario.filtrar_cidade('São Paulo')
    dias = fichario.get_columnEntries('Dia', agrupar=False)
    tempMax = fichario.get_columnEntries('Temp Max', agrupar=False)

    x_axis, y_axis = [], []

    for i in range(len(dias)):
        x_axis.append(float(i))
    for i in tempMax:
        y_axis.append(float(i))

    dados = fichario.get_dados()

    with dpg.plot(label="Temperatura", height=400, width=800):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        # Cria as labels do eixo x
        x_label = []
        for i in x_axis:
            x_label.append((dias[int(i)], i))
        x_label = tuple(x_label)
        print(x_label)
        dpg.add_plot_axis(dpg.mvXAxis, label="Dia")
        dpg.set_axis_ticks(dpg.last_item(),x_label)
        dpg.add_plot_axis(dpg.mvYAxis, label="Temp. Max", tag="y_axis")

        # Cria a linha de Temperatura máxima
        dpg.add_line_series(x_axis, y_axis, label="Temperatura Máxima", parent="y_axis")

dpg.create_viewport(title='PI6SEM', x_pos=0, y_pos=0)
dpg.set_primary_window(Tag.WindowPrimary, True)
dpg.setup_dearpygui()
dpg.show_viewport(maximized=True)
dpg.start_dearpygui()
dpg.destroy_context()