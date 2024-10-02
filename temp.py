import os, re
import pandas as pd

# file = open('./dados/areaUrbana.txt', 'r', encoding='utf-8')
# saida = open('./dados_tratados/areaUrbana.csv', '+a', encoding="utf-8")
# for linha in file.readlines():
#     linha = linha.replace(',','.')
#     linha = linha.replace('\t', ',')
#     linha = re.sub('[0-9]+,', "", linha)
#     saida.write(linha)

# siglas = {
#     " Acre":	'AC',
#     " Alagoas":	'AL',
#     " Amapá": 'AP',
#     " Amazonas":	'AM',
#     " Bahia": "BA",
#     " Ceará": "CE",
#     " Espírito Santo": "ES",
#     " Goiás": "GO",
#     " Maranhão":	"MA",
#     " Mato Grosso": "MT",
#     " Mato Grosso do Sul": "MS",
#     " Minas Gerais":	"MG",
#     " Pará":	"PA",
#     " Paraíba":	"PB",
#     " Paraná": "PR",
#     " Pernambuco": "PE",
#     " Piauí": "PI",
#     " Rio de Janeiro": "RJ",
#     " Rio Grande do Norte": "RN",
#     " Rio Grande do Sul": "RS",
#     " Rondônia":	"RO",
#     " Roraima": "RR",
#     " Santa Catarina": "SC",
#     " São Paulo": "SP",
#     " Sergipe": "SE",
#     " Tocantins": "TO",
#     " Distrito Federal": "DF"
# }

# file = pd.read_csv('./dados_tratados/areaUrbana.csv')
# file['Estado'] = file['Estado'].map(siglas)
# file.to_csv('./dados_tratados/areaUrbana.csv', sep=',')