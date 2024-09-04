import csv
import scrapy
from datetime import datetime, timezone, timedelta, datetime

class ClimaScrapper(scrapy.Spider):
    name = 'clima'

    start_urls = ['https://g1.globo.com/previsao-do-tempo/indice/']

    def parse(self, response):
        for i in range(65,91):#A até Z
            letter = str.lower(chr(i))
            cidades = response.css(f'div.desktop > section#index-{letter} > ul > li')

            for cidade in cidades:
            #cidade = cidades[0]
                link = cidade.css('a::attr(href)').extract_first()
                yield response.follow(link, self.parse_cidade)

    def parse_cidade(self, response):
        try:
            yield {
                'Cidade': response.css('div > div > p.forecast-header__place::text').get().split(',')[0],
                'Estado': response.css('div > div > p.forecast-header__place::text').get().split(',')[1],
                'Temp Max': response.css('div > div.forecast-today > div:nth-child(4) > div.forecast-today__temperature--max::text').get(),
                'Temp Min': response.css('div > div.forecast-today > div:nth-child(4) > div.forecast-today__temperature--min::text').get(),
                'Umidade': response.css('div > div.forecast-today-detail > div > div:nth-child(2) > div:nth-child(4) > span:nth-child(3)::text').get(),
                'Umidade Min': response.css('div > div.forecast-today-detail > div > div:nth-child(2) > div:nth-child(4) > span:nth-child(4)::text').get()
            }
        except:
            pass