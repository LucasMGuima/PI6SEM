import fichario as f
import my_window
import dearpygui.dearpygui as dpg

class WindowTemperatura(my_window.myWindow):
    def __init__(self, fichario: f.Fichario, estado:str = "SP", cidade: str = "São Paulo") -> None:
        self.id = id(self)
        self.fichario = fichario
        self.cidade = cidade
        self.estado = estado

        #Tags
        self.tagWPlot = f"wPlot {self.id}"
        self.tagYAxis = f"yAxis {self.id}"
        self.tagYTempMin = f"yTempMin {self.id}"
        self.tagYTempMax = f"yTempMax {self.id}"
        self.tagInpCidade = f"inpCidade {self.id}"
        self.tagInpEstado = f"inpEstado {self.id}"
        self.tagInpPeriodo = f"inpPeriodo {self.id}"

    def criar_janela(self) -> None:
        """
            Cria o painel contendo o gráfico de temperatura
        """

        #Painel de plot
        self.fichario.filtrar_cidade('São Paulo')
        dias = self.fichario.get_columnEntries('Dia', agrupar=False)
        tempMax = self.fichario.get_columnEntries('Temp Max', agrupar=False)
        tempMin = self.fichario.get_columnEntries('Temp Min', agrupar=False)
        #Remove o filtro do fichario 
        self.fichario.limpar_filtros()

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
        with dpg.window(label="Gráfico de Temperatura",width=850,height=450):
            with dpg.group(horizontal=True):
                with dpg.plot(tag=self.tagWPlot, label=f"Temperatura de(o) {self.cidade},{self.estado}", height=400, width=600):
                    # optionally create legend
                    dpg.add_plot_legend()

                    # REQUIRED: create x and y axes
                    dpg.add_plot_axis(dpg.mvXAxis, label="Data (Dia/Mês)")
                    dpg.set_axis_ticks(dpg.last_item(),x_label)
                    dpg.add_plot_axis(dpg.mvYAxis, label="Temperatura em °C", tag=self.tagYAxis)

                    # Cria a linha de Temperatura máxima
                    dpg.add_line_series(x_axis, tempMax, label="Temp. Máxima", parent=self.tagYAxis, tag=self.tagYTempMax)
                    # Cria a linha de Temperatura minima
                    dpg.add_line_series(x_axis, tempMin, label="Temp. Mínima", parent=self.tagYAxis, tag=self.tagYTempMin)
                
                with dpg.group():
                    with dpg.group(horizontal=True):
                        dpg.add_text('Estado: ')
                        dpg.add_input_text(tag=self.tagInpEstado, width=100)
                    dpg.add_separator()
                    with dpg.group(horizontal=True):
                        dpg.add_text('Cidade: ')
                        dpg.add_input_text(tag=self.tagInpCidade, width=100)
                    dpg.add_separator()
                    dpg.add_button(label="Mostrar", callback=self._atualizar_painel)

    def _atualizar_painel(self) -> None:
        #Atualiza os dados no mainel
        self.cidade = dpg.get_value(self.tagInpCidade)
        self.estado = dpg.get_value(self.tagInpEstado)
        #Painel de plot
        if not self.fichario.filtrar_estado(self.estado): return
        if not self.fichario.filtrar_cidade(self.cidade): return
        dias = self.fichario.get_columnEntries('Dia', agrupar=False)
        tempMax = self.fichario.get_columnEntries('Temp Max', agrupar=False)
        tempMin = self.fichario.get_columnEntries('Temp Min', agrupar=False)
        #Remove o filtro do fichario 
        self.fichario.limpar_filtros()

        x_axis = []

        for i in range(len(dias)):
            x_axis.append(float(i))
        # Cria as labels do eixo x
        x_label = []
        for i in x_axis:
            x_label.append((str(dias[int(i)]).replace('/2024', ''), i))
        x_label = tuple(x_label)

        dpg.configure_item(self.tagWPlot, label=f"Temperatura de(o) {self.cidade}, {self.estado}")
        dpg.set_value(self.tagYTempMax, [x_axis, tempMax])
        dpg.set_value(self.tagYTempMin, [x_axis, tempMin])