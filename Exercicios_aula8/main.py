from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

likes_count = 0
abas = ["curtidas", "jupiter", "professor"]
aba_atual_index = 0

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"aba_ativa": abas[aba_atual_index]}
    )

@app.post("/curtir", response_class=HTMLResponse)
def adicionar_curtida():
    global likes_count
    likes_count += 1
    return str(likes_count)

@app.delete("/curtir", response_class=HTMLResponse)
def zerar_curtidas():
    global likes_count
    likes_count = 0
    return str(likes_count)

@app.get("/abas/{nome_aba}", response_class=HTMLResponse)
def pegar_aba(request: Request, nome_aba: str):
    global aba_atual_index
    if nome_aba in abas:
        aba_atual_index = abas.index(nome_aba)
    
    return templates.TemplateResponse(
        request=request, 
        name=f"{nome_aba}.html", 
        context={"likes_count": likes_count, "aba_ativa": nome_aba}
    )

@app.get("/proxima-aba", response_class=HTMLResponse)
def proxima_aba(request: Request):
    global aba_atual_index
    aba_atual_index = (aba_atual_index + 1) % len(abas)
    nome_proxima_aba = abas[aba_atual_index]
    
    return templates.TemplateResponse(
        request=request,
        name=f"{nome_proxima_aba}.html", 
        context={"likes_count": likes_count, "aba_ativa": nome_proxima_aba}
    )