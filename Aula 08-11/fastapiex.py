from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    nome : str
    valor : float
    is_oferta : Union[bool,None] = None

@app.get("/")
async def read_root():
    return {"msg" : "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, nome: Union[str,None] = None):
    return {"item_id": item_id, "nome" : nome}

@app.put("/itens/{item_id}")
def atualiza_item(item_id: int, item: Item):
    return {"item_nome": item.nome, "item_id": item_id}