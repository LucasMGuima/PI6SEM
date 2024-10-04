import pandas as pd
import dearpygui.dearpygui as dpg
import os, threading, interface.w_tabela as w_tabela, interface.w_temperatura as w_temperatura, operacoes.fichario as f
import interface.operacoes as op

from interface.ref import Tag, Label, UR, Meses
from datetime import date

global fichario
global pieExist

pieExist = False
fichario = f.Fichario(pd.read_csv('./dados_tratados/dados.csv', index_col=0))

# Funcoes internas
def _run_coleta():
    fichario = op.run_coleta()

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
    dpg.delete_item(Tag.pieArea)
    
    with dpg.plot(label="Dias e Umidade Relativa do Ar",
                   height=250, width=500, 
                   tag=Tag.pieArea, 
                   parent=Tag.slot2):
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
        dpg.add_plot_legend(location=8, outside=True)

        dpg.add_plot_axis(dpg.mvXAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
        dpg.set_axis_limits(dpg.last_item(), 0, 1)

        with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
            dpg.set_axis_limits(dpg.last_item(), 0, 1)
            dpg.add_pie_series(0.5, 0.5, 0.5, values, labels, tag=Tag.piePlot)

def _carregarDados() -> None:
    """
        Carrega os dados da cidade/estado especificado na tela
    """
    
    estado: str = dpg.get_value(Tag.ComboEstado)
    cidade: str = dpg.get_value(Tag.ComboCidade)

    ini_mes = dpg.get_value(Tag.ComboMesIni)
    ini_dia = dpg.get_value(Tag.ComboDiaIni)
    fim_mes = dpg.get_value(Tag.ComboMesIni)
    fim_dia = dpg.get_value(Tag.ComboDiaFim)

    if(ini_mes and ini_dia and fim_mes and fim_dia): # Entrou com um intervalo de datas
        # Certifica que o mes está em formato numerico
        if(type(ini_mes) == str): ini_mes = Meses.get_mesNumber(Meses, ini_mes)
        if(type(fim_mes) == str): fim_mes = Meses.get_mesNumber(Meses, fim_mes)
        
        data_ini: str = f"{ini_dia}/{ini_mes}/2024"
        data_fim: str = f"{fim_dia}/{fim_mes}/2024"

        fichario.intarvalo_datas(data_ini, data_fim)
    elif(ini_mes and fim_mes and (not fim_dia or not ini_dia)): # Invervalo entre meses completos    
        # Certifica que o mes está em formato numerico
        if(type(ini_mes) == str): ini_mes = Meses.get_mesNumber(Meses, ini_mes)
        if(type(fim_mes) == str): fim_mes = Meses.get_mesNumber(Meses, fim_mes)
        
        ini_dia = 1
        fim_dia = Meses.get_mesDias(Meses, fim_mes)

        data_ini: str = f"{ini_dia}/{ini_mes}/2024"
        data_fim: str = f"{fim_dia}/{fim_mes}/2024"

        fichario.intarvalo_datas(data_ini, data_fim)

    if(not estado): return # Se não tiver estado selecionada sai

    if fichario.filtrar_estado(estado):
        if(cidade): fichario.filtrar_cidade(cidade)

        dias = fichario.get_columnEntries('Dia', agrupar=False)
        tempMax = fichario.get_columnEntries('Temp Max', agrupar=False)
        tempMin = fichario.get_columnEntries('Temp Min', agrupar=False)

        _creat_pieChart()
        _medias_amplitude()

        fichario.limpar_filtros()
        x_axis = []

        for i in range(len(dias)):
            x_axis.append(float(i))

        dpg.set_value(Tag.plotYTempMax, [x_axis, tempMax])
        dpg.set_value(Tag.plotYTempMin, [x_axis, tempMin])

def _medias_amplitude() -> None:
    dpg.delete_item(Tag.medidas)

    with dpg.group(tag=Tag.medidas, parent=Tag.slot3):
        dpg.add_text("MÉDIAS")
        dpg.add_text(f"Temperatura: {op.calc_tempMedia(fichario)}°C")
        dpg.add_text(f"Umidade: {op.calc_umiMedia(fichario)}%")
        dpg.add_separator()
        dpg.add_text(f"Amplitude térmica: {op.calc_ampliTemp(fichario)}°C")

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

def callback_populateDias(sender, app_data):
    # app_data -> valor celecionado na combo
    # sender -> tag de quen chamou o callback
    lst_dias = []
    
    mes_num = Meses.get_mesNumber(Meses, app_data)
    datas = fichario.get_columnEntries('Dia')
    
    for data in datas:
        d_mes = str(data).split('/')[1]
        if(int(mes_num) == int(d_mes)): lst_dias.append(str(data).split('/')[0])

    if(sender == Tag.ComboMesIni):
        # Popula o combo de dias de inicio
        dpg.configure_item(Tag.ComboDiaIni, items=lst_dias)
        return
    
    if(sender == Tag.ComboMesFim):
        # Popula o combo de dias de fim
        dpg.configure_item(Tag.ComboDiaFim, items=lst_dias)
        return

# Funcoes de paines
def painel_configPesquisa():
    with dpg.child_window(width=250):
        dpg.add_text("Dados de pesquisa")
        dpg.add_separator()
        with dpg.group():
            _criarCombo(Tag.ComboEstado, Label.InpTextEstado, fichario.get_columnEntries('Estado'), _get_cidadePorEstado)
            _criarCombo(Tag.ComboCidade, Label.InpTextCidade)
            dpg.add_separator()
            dpg.add_text("Periodo")
            dpg.add_separator()
            meses_inTable = fichario.get_columnEntries('Dia')
            lst_nomeMeses = []
            for el in meses_inTable:
                mes_num = str(el).split('/')[1]
                mes_nome = Meses.get_mesNome(Meses, int(mes_num))
                if mes_nome not in lst_nomeMeses: lst_nomeMeses.append(mes_nome) 
            with dpg.group():
                dpg.add_text("De: ")
                with dpg.group(horizontal=True):
                    dpg.add_text("Mes:")
                    dpg.add_combo(tag=Tag.ComboMesIni,items=lst_nomeMeses, width=100, callback=callback_populateDias)
                    dpg.add_text("Dia:")
                    dpg.add_combo(tag=Tag.ComboDiaIni,width=50)
            with dpg.group():
                dpg.add_text("Até: ")
                with dpg.group(horizontal=True):
                    dpg.add_text("Mes:")
                    dpg.add_combo(tag=Tag.ComboMesFim,items=lst_nomeMeses, width=100, callback=callback_populateDias)
                    dpg.add_text("Dia:")
                    dpg.add_combo(tag=Tag.ComboDiaFim,width=50)
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
                with dpg.child_window(height=270, width=500, tag=Tag.slot2):
                    _creat_pieChart()
                with dpg.child_window(height=270, width=200, tag=Tag.slot3):
                    _medias_amplitude()
        
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