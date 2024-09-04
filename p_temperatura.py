import fichario as f
import dearpygui.dearpygui as dpg

class painelTemperatura():
    def __init__(self, fichario: f.Fichario, cidade: str = "São Paulo") -> None:
        self.fichario = fichario
        self.cidade = cidade

    def criar_painel(self) -> None:
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

        with dpg.plot(tag='window plot', label=f"Temperatura de(o) {self.cidade}", height=400, width=800):
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
        
        with dpg.group(horizontal=True):
            dpg.add_text('Cidade: ')
            dpg.add_input_text(tag="Cidade", width=200)
            dpg.add_button(label="Mudar", callback=self.atualizar_painel)

    def atualizar_painel(self) -> None:
        self.cidade = dpg.get_value("Cidade")
        #Painel de plot
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

        dpg.configure_item("window plot", label=f"Temperatura de(o) {self.cidade}")
        dpg.set_value('yAxis Temp. Max', [x_axis, tempMax])
        dpg.set_value('yAxis Temp. Min', [x_axis, tempMin])