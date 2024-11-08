import pytesseract
from PIL import Image

# Carregar a imagem
image = Image.open("img.png")

# Extrair texto da imagem
text = pytesseract.image_to_string(image, lang='por')
print("Texto extraído:", text)
