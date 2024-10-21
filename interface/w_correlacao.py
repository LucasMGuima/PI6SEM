from scipy.stats import pearsonr

import fichario as f
import interface.my_window as my_window
import dearpygui.dearpygui as dpg
import pandas as pd
import math

class WindowCorrelacoes(my_window.myWindow):
    def __init__(self, fichario: f.Fichario, estado: str = "SP", cidade: str = "São Paulo") -> None:
        self.id = id(self)
        self.estado = estado
        self.cidade = cidade
        self.fichario = fichario

        self.area_urbana = pd.read_csv("./dados_tratados/areaUrbana.csv")
        self.area_urbana = self.area_urbana.sort_values(by=['AreaUrbana'], ascending=False)
        print(self.area_urbana)

        super().__init__()

    def criar_janela(self) -> None:
        with dpg.window(label="UmidadeXTemperatura",
                        tag=300,
                        width=600, height=500,
                        on_close= lambda: dpg.delete_item(300)):
            with dpg.group(horizontal=True):
                cidades = self.fichario.get_columnEntries('Cidade')

                dados = []
                for cidade in cidades:
                    self.fichario.filtrar_cidade(cidade)
                    cidade_dados = self.fichario.get_dados()
                    estado = self.fichario.get_columnEntries('Estado')
                    self.fichario.limpar_filtros()

                    humi_med = cidade_dados['Umidade']
                    sum = 0
                    for humi in humi_med: sum += int(humi)
                    media_Umidade = math.floor(sum/len(humi_med))

                    temp_med = cidade_dados['Temp Med']
                    sum = 0
                    for temp in temp_med: sum += int(temp)
                    media = math.floor(sum/len(temp_med))

                    area_urbana = self.area_urbana.loc[(self.area_urbana['Cidade'] == cidade) & (self.area_urbana['Estado'] == estado[0])]
                    
                    if(area_urbana.empty == False):
                        new_row = (cidade, estado[0], media, media_Umidade, area_urbana['AreaUrbana'].values[0])
                        dados.append(new_row)
                dados_agrupados = pd.DataFrame(dados, columns=['Cidade', 'Estado', 'Temp Media', 'Umidade', 'Area Urbana'])
                corr1, pvalor = pearsonr(dados_agrupados['Temp Media'], dados_agrupados['Umidade'])
                corr2, pvalor = pearsonr(dados_agrupados['Umidade'], dados_agrupados['Area Urbana'])
                corr3, pvalor = pearsonr(dados_agrupados['Temp Media'], dados_agrupados['Area Urbana'])

                with dpg.plot():
                    dpg.add_plot_axis(dpg.mvXAxis, label="Temp. Média")
                    dpg.add_plot_axis(dpg.mvYAxis, label='Umidade', tag=304)
                    for cidade in dados_agrupados['Cidade']:
                        row = dados_agrupados.loc[(dados_agrupados['Cidade'] == cidade)]
                        print(row)
                        dpg.add_scatter_series(row['Temp Media'].values[0], row['Umidade'].values[0], parent=304)

                with dpg.group(horizontal=False):
                    dpg.add_text("Correlação entre Temperatura e Umidade: %.3f" % corr1)
                    dpg.add_text("Correlação entre Umidade e Area Urbana: %.3f" % corr2)
                    dpg.add_text("Correlação entre Temperatura e Area Urbana: %.3f" % corr3)

                