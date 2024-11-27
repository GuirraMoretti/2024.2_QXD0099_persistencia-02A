"""
Implementação Completa de um Extrator de Dados Estruturados e Não Estruturados
Objetivo: Integrar conhecimentos e simular um fluxo completo de extração de dados.
Tarefa: Escreva um código que possa extrair dados de um site (HTML), de um PDF e de uma imagem.
O código deve identificar o tipo de cada arquivo, extrair as informações relevantes e exibi-las em um formato organizado.
"""

import os

def extract_image(file):
    #Importando Lib
    import pytesseract
    from PIL import Image as img
    #Importando Lib

    image = img.open(file)
    txt_img = pytesseract.image_to_string(image)
    return txt_img

def extract_html(site):
    #Importando Lib
    from bs4 import BeautifulSoup as soup
    import requests
    #Importando Lib
    
    site = "https://" + site
    response = requests.get(site)
    doc = soup(response.content, "html.parser")
    html_str = doc.prettify()
    return html_str

def extract_pdf(file):
    #Importando Lib
    from pdfminer.high_level import extract_text
    #Importando Lib
    return extract_text(file)

def write_in_txt(text):
    with open("texto_imagem.txt","w",encoding="utf-8") as file:
        file.write(text)


def main():
    x = input('Qual arquivo deseja carregar?:\n(1)Site\n(2)Arquivo(PDF ou PNG)\n>')
    match x:
        case '1':
            site = input('Digite o url do site(Sem https):\n>')
            x = extract_html(site)
        case '2':
            file = input(f'Você está no diretorio = ({os.getcwd()})\nDigite o caminho do arquivo:\n>')
            if not os.path.exists(file):
                return print("Arquivo não existe")
            if file.endswith('.png'):
                x = extract_image(file)
            elif file.endswith('.pdf'):
                x = extract_pdf(file)
            else:
                print('Tipo de arquivo não suportado')
    write_in_txt(x)

if __name__ == "__main__":
    main()