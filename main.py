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

def mudar():
    global fichario

    #Painel de plot
    fichario.filtrar_cidade('Rio de Janeiro')
    dias = fichario.get_columnEntries('Dia', agrupar=False)
    tempMax = fichario.get_columnEntries('Temp Max', agrupar=False)
    tempMin = fichario.get_columnEntries('Temp Min', agrupar=False)
    #Remove o filtro do fichario 
    fichario.limpar_filtros()

    x_axis = []

    for i in range(len(dias)):
        x_axis.append(float(i))
    # Cria as labels do eixo x
    x_label = []
    for i in x_axis:
        x_label.append((str(dias[int(i)]).replace('/2024', ''), i))
    x_label = tuple(x_label)

    dpg.configure_item("window plot", label="Temperatura do Rio de Janeiro")
    dpg.set_value('yAxis Temp. Max', [x_axis, tempMax])
    dpg.set_value('yAxis Temp. Min', [x_axis, tempMin])

def painel_temperatura():
    global fichario

    #Painel de plot
    fichario.filtrar_cidade('São Paulo')
    dias = fichario.get_columnEntries('Dia', agrupar=False)
    tempMax = fichario.get_columnEntries('Temp Max', agrupar=False)
    tempMin = fichario.get_columnEntries('Temp Min', agrupar=False)
    #Remove o filtro do fichario 
    fichario.limpar_filtros()

    x_axis, y_axis = [], []

    #Junta as duas temperaturas e remove repetições
    temperatura = list(set(tempMax + tempMin))
    temperatura.sort()

    for i in range(len(dias)):
        x_axis.append(float(i))
    # Cria as labels do eixo x
    x_label = []
    for i in x_axis:
        x_label.append((str(dias[int(i)]).replace('/2024', ''), i))
    x_label = tuple(x_label)

    for i in temperatura:
        y_axis.append(float(i))

    with dpg.plot(tag='window plot', label="Temperatura de São Paulo", height=400, width=800):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="Data (Dia/Mês)")
        dpg.set_axis_ticks(dpg.last_item(),x_label)
        dpg.add_plot_axis(dpg.mvYAxis, label="Temperatura em °C", tag="y_axis")

        # Cria a linha de Temperatura máxima
        dpg.add_line_series(x_axis, tempMax, label="Temp. Máxima", parent="y_axis", tag="yAxis Temp. Max")
        # Cria a linha de Temperatura minima
        dpg.add_line_series(x_axis, tempMin, label="Temp. Mínima", parent="y_axis", tag="yAxis Temp. Min")

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
    
    painel_temperatura()
    dpg.add_button(label="Mudar", callback=mudar)
    
    

dpg.create_viewport(title='PI6SEM', x_pos=0, y_pos=0)
dpg.set_primary_window(Tag.WindowPrimary, True)
dpg.setup_dearpygui()
dpg.show_viewport(maximized=True)
dpg.start_dearpygui()
dpg.destroy_context()