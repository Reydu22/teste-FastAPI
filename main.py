from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

usuarios = {}

class Usuario(BaseModel):
    nome: str
    idade: int


@app.post("/usuarios")
def criar(usuario: Usuario):
    usuario_id = len(usuarios) + 1
    usuarios[usuario_id] = {"Nome": {usuario.nome}, "Idade": {usuario.idade}}
    return f"Usuario {usuario.nome} adicionado no Banco de Dados"

@app.get("/usuarios")
def root():
    return usuarios