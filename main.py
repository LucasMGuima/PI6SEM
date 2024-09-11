import pandas as pd
import dearpygui.dearpygui as dpg
import os, threading, w_tabela, w_temperatura, fichario as f

from ref import Tag, Label, UR
from datetime import date

global fichario
global pieExist

pieExist = False
fichario = f.Fichario(pd.read_csv('./dados_tratados/dados.csv', index_col=0))

# Funcoes internas
def _run_coleta():
    os.system("python .\operacoes\coletar_dados.py")
    os.system("python .\operacoes\\tratar_dados.py")
    global fichario
    fichario = f.Fichario(pd.read_csv('./dados_tratados/dados.csv', index_col=0))

def _criarCombo(tag: int | str, label: str = "", items: list[str] | tuple[str, ...] = (), callback=None) -> None:
    with dpg.group(horizontal=True):
        if(len(label) > 0): dpg.add_text(label)
        dpg.add_combo(items=items, tag=tag, callback=callback)

def _get_cidadePorEstado() -> list[str]:
    estado: str = dpg.get_value(Tag.ComboEstado)
    if(fichario.filtrar_estado(estado)):
        cidades = fichario.get_columnEntries('Cidade')
        cidades.sort()
        fichario.limpar_filtros()
        dpg.configure_item(Tag.ComboCidade, items=cidades)

def _creat_pieChart() -> None:
    global pieExist
    if(pieExist): 
        dpg.delete_item("pie")
    else: pieExist = True
    
    with dpg.plot(label="Total de dias em relação a Umidade Relativa do Ar", height=250, tag="pie", parent="slot_2"):
        x_axis = fichario.get_columnEntries("Qualidade UR")
        y_axis = fichario.get_columnEntries("Qualidade UR", agrupar=False)

        values = []
        for x in x_axis:
            count = 0
            for y in y_axis:
                if x == y: count += 1
            percent = (count*100)/(len(y_axis))
            values.append(percent)
        
        labels = []
        for x in x_axis:
            labels.append(UR.qualidade[x])
        
        # create legend
        dpg.add_plot_legend()

        dpg.add_plot_axis(dpg.mvXAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
        dpg.set_axis_limits(dpg.last_item(), 0, 1)

        with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
            dpg.set_axis_limits(dpg.last_item(), 0, 1)
            dpg.add_pie_series(0.5, 0.5, 0.25, values, labels, tag=Tag.piePlot)

def _carregarDados() -> None:
    """
        Carrega os dados da cidade/estado especificado na tela
    """
    
    estado: str = dpg.get_value(Tag.ComboEstado)
    cidade: str = dpg.get_value(Tag.ComboCidade)

    if(not estado): return # Se não tiver estado selecionada sai

    if fichario.filtrar_estado(estado):
        if(cidade): fichario.filtrar_cidade(cidade)

        dias = fichario.get_columnEntries('Dia', agrupar=False)
        tempMax = fichario.get_columnEntries('Temp Max', agrupar=False)
        tempMin = fichario.get_columnEntries('Temp Min', agrupar=False)

        _creat_pieChart()

        fichario.limpar_filtros()
        x_axis = []

        for i in range(len(dias)):
            x_axis.append(float(i))

        dpg.set_value(Tag.plotYTempMax, [x_axis, tempMax])
        dpg.set_value(Tag.plotYTempMin, [x_axis, tempMin])



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
        dpg.add_separator()
        with dpg.group():
            _criarCombo(Tag.ComboEstado, Label.InpTextEstado, fichario.get_columnEntries('Estado'), _get_cidadePorEstado)
            _criarCombo(Tag.ComboCidade, Label.InpTextCidade)
            #dpg.add_separator()
            #dpg.add_text("Periodo")
            #dpg.add_separator()
            #with dpg.group(horizontal=True):
            #    dpg.add_text("De: ")
            #    dpg.add_combo()
            #with dpg.group(horizontal=True):
            #    dpg.add_text("Até: ")
            #    dpg.add_combo()
            dpg.add_button(label="Mostrar", callback=_carregarDados)

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
                with dpg.child_window(height=270, width=500, tag="slot_2"):
                    _creat_pieChart()
                with dpg.child_window(height=270, width=200):
                    dpg.add_text("Medias/Amplitude")
        
            with dpg.child_window(height=350):
                with dpg.plot(tag=Tag.plotTempUmidade, width=700):
                    #Painel de plot
                    fichario.filtrar_cidade('São Paulo')
                    dias = fichario.get_columnEntries('Dia', agrupar=False)
                    tempMax = fichario.get_columnEntries('Temp Max', agrupar=False)
                    tempMin = fichario.get_columnEntries('Temp Min', agrupar=False)
                    
                    fichario.limpar_filtros()

                    x_axis = []

                    for i in range(len(dias)):
                        x_axis.append(float(i))
                    # Cria as labels do eixo x
                    x_label = []
                    for i in x_axis:
                        x_label.append((str(dias[int(i)]).replace('/2024', ''), i))
                    x_label = tuple(x_label)

                    # optionally create legend
                    dpg.add_plot_legend()

                    # REQUIRED: create x and y axes
                    dpg.add_plot_axis(dpg.mvXAxis, label="Data (Dia/Mês)")
                    dpg.set_axis_ticks(dpg.last_item(),x_label)
                    dpg.add_plot_axis(dpg.mvYAxis, label="Temperatura em °C", tag=Tag.plotYAxis)

                    # Cria a linha de Temperatura máxima
                    dpg.add_line_series(x_axis, tempMax, label="Temp. Máxima", parent=Tag.plotYAxis, tag=Tag.plotYTempMax)
                    # Cria a linha de Temperatura minima
                    dpg.add_line_series(x_axis, tempMin, label="Temp. Mínima", parent=Tag.plotYAxis, tag=Tag.plotYTempMin)

dpg.create_viewport(title='PI6SEM', width=1000, height=700, x_pos=0, y_pos=0)
dpg.set_primary_window(Tag.WindowPrimary, True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()