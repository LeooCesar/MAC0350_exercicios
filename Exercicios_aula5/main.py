from fastapi import FastAPI, Request, Response, HTTPException, Depends, Cookie
from typing import Annotated
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


app = FastAPI()

#Monta a pasta "static" na rota "/static"
app.mount("/static", StaticFiles(directory="static"), name="static")

#Sintaxe recomendada: diretório como primeiro argumento posicional
templates = Jinja2Templates(directory="templates")

users_db = []

class User(BaseModel):
    nome: str 
    bio: str
    senha: str

class LoginData(BaseModel):
    nome: str
    senha: str

@app.get("/", response_class=HTMLResponse)
def pagina_de_cadastro(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="cadastro.html"
    )
@app.post("/users")
def criar_usuario_novo(user: User):
    users_db.append(user.model_dump())
    return {"mensagem": f"Usuário {user.nome} criado com sucesso!"}

@app.get("/login", response_class=HTMLResponse)
def pagina_de_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name= "login.html"
    )

@app.post("/login")
def fazer_login(dados: LoginData, response: Response):
    usuario_encontrado = None
    for u in users_db:
        if u["nome"] == dados.nome and u["senha"] == dados.senha:
            usuario_encontrado = u
            break
    if not usuario_encontrado:
        raise HTTPException(status_code=401, detail="Nome e/ou senha inconrretos")
    response.set_cookie(key="session_user", value=dados.nome)
    return {"mensagem": "Logado com sucesso!"}

def get_activate_user(session_user: Annotated[str | None, Cookie()] = None):
    if not session_user:
        raise HTTPException(status_code=401, detail="Você ainda não está logado")
    for u in users_db:
        if u["nome"] == session_user:
            return u
        
    raise HTTPException(status_code=401, detail="Sessão inválida.")

@app.get("/home", response_class=HTMLResponse)
def pagina_home(request: Request, user: dict = Depends(get_activate_user)):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"user": user}
    )

