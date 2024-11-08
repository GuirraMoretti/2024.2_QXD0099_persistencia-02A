from bs4 import BeautifulSoup
import requests

# Conexão com a página e extração do título
response = requests.get("https://quixada.ufc.br")
doc = BeautifulSoup(response.content, "html.parser")
title = doc.title.string
