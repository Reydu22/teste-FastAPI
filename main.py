from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os 

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
app = FastAPI()

usuarios = {}
class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    idade = Column(Integer)

Base.metadata.create_all(bind=engine)

class Usuario(BaseModel):
    nome: str
    idade: int

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@app.post("/usuarios")
def criar(usuario: Usuario):
    db = next(get_db())
    db_usuario = UsuarioDB(nome=usuario.nome,idade=usuario.idade)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    #usuarios[usuario_id] = {"Nome": {usuario.nome}, "Idade": {usuario.idade}}
    return f"Usuario {usuario.nome} adicionado no Banco de Dados"

@app.get("/usuarios")
def root():
    db = next(get_db())
    usuarios = db.query(UsuarioDB).all()
    return [{f'ID: {u.id} Nome: {u.nome} Idade: {u.idade}' for u in usuarios}]

@app.get("/usuarios/{id}")
def buscar(id: int):
    db = next(get_db())
    usuarios = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    u = usuarios
    print(u)
    if u == None:
        return 'usuario não encontrado'
    return [{f'ID: {u.id} Nome: {u.nome} Idade: {u.idade}'}]

@app.delete("/usuarios/{id}")
def deletar(id: int):
    db = next(get_db())
    usuarios = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    nome,idade,id = usuarios.nome,usuarios.idade,usuarios.id
    db.delete(usuarios)
    db.commit()
    return f'Usuarios de nome {nome}, Idade {idade} e ID {id} removido do Banco de Dados'
