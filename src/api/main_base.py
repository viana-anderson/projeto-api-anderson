from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()

# Banco de dados em memória
pedidos = []
next_id = 1

# Modelos
class Item(BaseModel):
    nome: str
    preco: float
    qtd: int

class PedidoCreate(BaseModel):
    cliente: str
    itens: List[Item]

class Pedido(BaseModel):
    id: int
    cliente: str
    itens: List[Item]
    total: float
    status: str
    criadoEm: datetime


STATUS_VALIDOS = ["PENDENTE", "PAGO", "ENVIADO", "FINALIZADO", "CANCELADO"]


@app.post("/pedidos", response_model=Pedido)
def criar_pedido(dados: PedidoCreate):
    global next_id

    # Cálculo total
    total = sum(item.preco * item.qtd for item in dados.itens)

    novoPedido = Pedido(
        id=next_id,
        cliente=dados.cliente,
        itens=dados.itens,
        total=total,
        status="PENDENTE",
        criadoEm=datetime.now()
    )

    pedidos.append(novoPedido)
    next_id += 1

    return novoPedido


@app.get("/pedidos", response_model=List[Pedido])
def listar_pedidos():
    return pedidos


@app.patch("/pedidos/{id}/status", response_model=Pedido)
def atualizar_status(id: int, status: str):
    # Busca pedido
    pedido = next((p for p in pedidos if p.id == id), None)

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if status not in STATUS_VALIDOS:
        raise HTTPException(status_code=400, detail="Status inválido")

    pedido.status = status

    return pedido


@app.get("/")
def home():
    return {"mensagem": "API de pedidos funcionando!"}
