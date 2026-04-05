from fastapi import FastAPI, Request, Form, Depends, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Função auxiliar para abrir e fechar a conexão com o banco a cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Página principal, mostrando os campeonatos do usuário
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    lista_de_campeonatos = db.query(models.Championship).all()

    return templates.TemplateResponse(
        request=request, 
        name="index.html",
        context={"campeonatos": lista_de_campeonatos}
    )

# Adiciona um campeonato na lista da página principal e também no banco de dados
@app.post("/campeonatos")
def criar_campeonato(
    request: Request,
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    novo_campeonato = models.Championship(name=name)
    db.add(novo_campeonato)
    db.commit()
    db.refresh(novo_campeonato)

    return templates.TemplateResponse(
        request=request,
        name="partials/campeonato_item.html",
        context={"campeonato": novo_campeonato}
    )

# Deleta o campeonato da lista da página principal e também do banco de dados
@app.delete("/campeonatos/{campeonato_id}")
def deletar_campeonato(campeonato_id: int, db: Session = Depends(get_db)):
    campeonato = db.query(models.Championship).filter(models.Championship.id == campeonato_id).first()

    if campeonato:
        db.delete(campeonato)
        db.commit()

    return Response(status_code=200)

# Mostra a tela do campeonato escolhido
@app.get("/campeonatos/{campeonato_id}")
def detalhes_campeonato(request: Request, campeonato_id: int, db: Session = Depends(get_db)):
    campeonato = db.query(models.Championship).filter(models.Championship.id == campeonato_id).first()
    total_partidas = len(campeonato.matches)
    vitorias = 0
    pontos_feitos = 0
    pontos_sofridos = 0

    for partida in campeonato.matches:
        if partida.our_score > partida.opponent_score:
            vitorias += 1
        for set_partida in partida.sets:
            pontos_feitos += set_partida.our_points
            pontos_sofridos += set_partida.opponent_points

    aproveitamento = (vitorias / total_partidas * 100) if total_partidas > 0 else 0
    saldo_pontos = pontos_feitos - pontos_sofridos

    estatisticas = {
        "total": total_partidas,
        "vitorias": vitorias,
        "derrotas": total_partidas - vitorias,
        "aproveitamento": f"{aproveitamento:.0f}%",
        "saldo": saldo_pontos
    }

    return templates.TemplateResponse(
        request=request,
        name="detalhes.html",
        context={"campeonato": campeonato, "stats": estatisticas}
    )

# Adiciona uma partida no campeonato escolhido
@app.post("/campeonatos/{campeonato_id}/partidas")
def adicionar_partida(
    request: Request,
    campeonato_id: int,
    category: str = Form(...),
    stage: str = Form(...),
    our_set1: int = Form(...),
    opp_set1: int = Form(...),
    our_set2: int = Form(...),
    opp_set2: int = Form(...),
    our_set3: int | None = Form(None), # Terceiro set é opcional
    opp_set3: int | None = Form(None), # Terceiro set é opcional
    partner: str | None = Form(None),  # Deixo isso como opcional, caso a pessoa vá jogar simples 
    opponents: str = Form(...),
    db: Session = Depends(get_db)
):
    
    our_total = 0
    opp_total = 0

    if our_set1 > opp_set1: our_total += 1
    else: opp_total += 1

    if our_set2 > opp_set2: our_total += 1
    else: opp_total += 1

    if our_set3 is not None and opp_set3 is not None:
        if our_set3 > opp_set3: our_total += 1
        else: opp_total += 1

    nova_partida = models.Match(
        championship_id=campeonato_id,
        category=category,
        stage=stage,
        our_score=our_total,
        opponent_score=opp_total,
        partner=partner,
        opponents=opponents
    )

    db.add(nova_partida)
    db.commit()
    db.refresh(nova_partida)

    set1 = models.MatchSet(match_id=nova_partida.id, our_points=our_set1, opponent_points=opp_set1)
    db.add(set1)

    set2 = models.MatchSet(match_id=nova_partida.id, our_points=our_set2, opponent_points=opp_set2)
    db.add(set2)

    if our_set3 is not None and opp_set3 is not None:
        set3 = models.MatchSet(match_id=nova_partida.id, our_points=our_set3, opponent_points=opp_set3)
        db.add(set3)

    db.commit()
    db.refresh(nova_partida)

    return templates.TemplateResponse(
        request=request,
        name="partials/partida_item.html",
        context={"partida": nova_partida}
    )

@app.get("/partidas/{partida_id}")
def visualizar_partida(request: Request, partida_id: int, db: Session = Depends(get_db)):
    partida = db.query(models.Match).filter(models.Match.id == partida_id).first()
    return templates.TemplateResponse(request=request, name="partials/partida_item.html", context={"partida": partida})


@app.get("/partidas/{partida_id}/editar")
def editar_partida_form(request: Request, partida_id: int, db: Session = Depends(get_db)):
    partida = db.query(models.Match).filter(models.Match.id == partida_id).first()
    
    set1 = partida.sets[0] if len(partida.sets) > 0 else None
    set2 = partida.sets[1] if len(partida.sets) > 1 else None
    set3 = partida.sets[2] if len(partida.sets) > 2 else None

    return templates.TemplateResponse(
        request=request,
        name="partials/partida_form_edit.html",
        context={"partida": partida, "set1": set1, "set2": set2, "set3": set3}
    )


@app.put("/partidas/{partida_id}")
def atualizar_partida(
    request: Request,
    partida_id: int,
    category: str = Form(...),
    stage: str = Form(...),
    our_set1: int = Form(...),
    opp_set1: int = Form(...),
    our_set2: int = Form(...),
    opp_set2: int = Form(...),
    our_set3: int | None = Form(None), 
    opp_set3: int | None = Form(None),
    partner: str | None = Form(None),
    opponents: str = Form(...),
    db: Session = Depends(get_db)
):
    partida = db.query(models.Match).filter(models.Match.id == partida_id).first()
    
    our_total = 0
    opp_total = 0
    if our_set1 > opp_set1: our_total += 1
    else: opp_total += 1
    if our_set2 > opp_set2: our_total += 1
    else: opp_total += 1
    if our_set3 is not None and opp_set3 is not None:
        if our_set3 > opp_set3: our_total += 1
        else: opp_total += 1

    partida.category = category
    partida.stage = stage
    partida.our_score = our_total
    partida.opponent_score = opp_total
    partida.partner = partner
    partida.opponents = opponents
    
    db.query(models.MatchSet).filter(models.MatchSet.match_id == partida.id).delete()
    db.add(models.MatchSet(match_id=partida.id, our_points=our_set1, opponent_points=opp_set1))
    db.add(models.MatchSet(match_id=partida.id, our_points=our_set2, opponent_points=opp_set2))
    if our_set3 is not None and opp_set3 is not None:
        db.add(models.MatchSet(match_id=partida.id, our_points=our_set3, opponent_points=opp_set3))

    db.commit()
    db.refresh(partida)

    return templates.TemplateResponse(request=request, name="partials/partida_item.html", context={"partida": partida})

# Deleta uma partida no campeonato escolhido e do banco de dados
@app.delete("/partidas/{partida_id}")
def deletar_partida(partida_id: int, db: Session = Depends(get_db)):
    partida = db.query(models.Match).filter(models.Match.id == partida_id).first()

    if partida:
        db.delete(partida)
        db.commit()

    return Response(status_code=200)
