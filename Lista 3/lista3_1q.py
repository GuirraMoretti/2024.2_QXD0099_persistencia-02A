from bs4 import BeautifulSoup as soup
import requests


"""
1. Scraping de Websites com BeautifulSoup
Objetivo: Praticar a extração de dados de um site usando scraping.
Tarefa: Usando a biblioteca BeautifulSoup, escreva um código que extraia e imprima o título e todos os links de uma página web. A URL pode ser qualquer página pública, como https://example.com.
"""

# Conexão com a página e extração do título
response = requests.get("https://quixada.ufc.br")
doc = soup(response.content, "html.parser")
print(f'Titulo: {doc.title.string}\n')

#Extração dos links
for link in doc.find_all('a'):
    print(link.get('href'))
