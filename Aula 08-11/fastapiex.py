from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    nome: str
    valor: float
    is_oferta: Union[bool, None] = None

# Dicionário para armazenar itens
items_db = {}

@app.get("/")
def read_root():
    return {"msg": "Hello World"}

@app.get("/itens/{item_id}")
def le_item(item_id: int):
    # Verifica se o item existe no dicionário
    if item_id in items_db:
        return items_db[item_id]
    else:
        return {"erro": "Item não encontrado"}

@app.put("/itens/{item_id}")
def atualiza_item(item_id: int, item: Item):
    # Salva o item no dicionário
    items_db[item_id] = item
    return {"mensagem": "Item atualizado com sucesso", "item": items_db[item_id]}
