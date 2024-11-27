"""
2. Extração de Texto de Imagens com OCR
Objetivo: Extrair texto de imagens usando OCR.
Tarefa: Usando pytesseract e PIL, escreva um código para carregar uma imagem, extrair o texto nela contido
e salvar o resultado num arquivo txt..
"""
import pytesseract
from PIL import Image as img

image = img.open("hino.png")
txt_img = pytesseract.image_to_string(image)

#Salvar texto da imagem
with open("texto_imagem.txt","x",encoding="utf-8") as file:
    file.write(txt_img)
    