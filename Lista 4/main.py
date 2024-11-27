import os
from typing import List
from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import xml.etree.ElementTree as ET

app = FastAPI()
XML_FILE = "livros.xml"

class Livro(BaseModel):
    id: int
    titulo: str
    autor: str
    ano: int
    genero: str

livros: List[Livro] = []

@app.on_event("startup")
def carregar_livros():
    global livros
    livros = ler_dados_xml()

@app.get("/")
def padrao():
    return {"msg": "API de Gerenciamento de Livros"}

def ler_dados_xml() -> List[Livro]:
    livros_list = []
    if os.path.exists(XML_FILE):
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        for elem in root.findall("livro"):
            try:
                livro = Livro(
                    id=int(elem.find("id").text),
                    titulo=elem.find("titulo").text,
                    autor=elem.find("autor").text,
                    ano=int(elem.find("ano").text),
                    genero=elem.find("genero").text,
                )
                livros_list.append(livro)
            except (AttributeError, ValueError) as e:
                # Log de erro ou tratamento adicional pode ser feito aqui
                continue
    return livros_list

def escrever_dados_xml(livros_para_escrever: List[Livro]):
    root = ET.Element("livros")
    for livro in livros_para_escrever:
        livro_elem = ET.SubElement(root, "livro")
        ET.SubElement(livro_elem, "id").text = str(livro.id)
        ET.SubElement(livro_elem, "titulo").text = livro.titulo
        ET.SubElement(livro_elem, "autor").text = livro.autor
        ET.SubElement(livro_elem, "ano").text = str(livro.ano)
        ET.SubElement(livro_elem, "genero").text = livro.genero
    tree = ET.ElementTree(root)
    tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)

# Listar todos os livros
@app.get("/livros/", response_model=List[Livro])
def listar_livros():
    return livros

# Buscar livro por ID
@app.get("/livros/{livro_id}", response_model=Livro)
def buscar_livro_por_id(livro_id: int):
    for livro in livros:
        if livro.id == livro_id:
            return livro
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Livro não encontrado.")

# Criar um novo livro
@app.post("/livros/", response_model=Livro, status_code=HTTPStatus.CREATED)
def adicionar_livro(livro: Livro):
    if any(l.id == livro.id for l in livros):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="ID já existe.")
    livros.append(livro)
    escrever_dados_xml(livros)
    return livro

# Atualizar um livro existente
@app.put("/livros/{livro_id}", response_model=Livro)
def atualizar_livro(livro_id: int, livro_atualizado: Livro):
    for indice, livro in enumerate(livros):
        if livro.id == livro_id:
            # Verifica se o ID no payload corresponde ao ID na URL
            if livro_atualizado.id != livro_id:
                if any(l.id == livro_atualizado.id for l in livros):
                    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="ID no payload já existe.")
            livros[indice] = livro_atualizado
            escrever_dados_xml(livros)
            return livro_atualizado
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Livro não encontrado.")

# Deletar um livro
@app.delete("/livros/{livro_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_livro(livro_id: int):
    for indice, livro in enumerate(livros):
        if livro.id == livro_id:
            del livros[indice]
            escrever_dados_xml(livros)
            return
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Livro não encontrado.")
