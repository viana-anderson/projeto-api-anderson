"""
Aplicação FastAPI principal
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel 
from typing import List
from datetime import datetime
from src.data.schemas import Item, PedidoCreate, Pedido


# Criar instância do FastAPI
app = FastAPI(
    title="PROJETO API",
    version="1.0.0",
    description="API de Lógica de Negócio: Sistema de Consulta a Produtos",
)


@app.get("/")
def root():
    """
    Endpoint raiz - mensagem de boas-vindas
    """
    return {"message": "API está no ar!"}


@app.get("/health")
def health_check():
    """
    Health check - verifica se API está funcionando
    """
    return {"status": "healthy", "version": "1.0.0"}


# Banco de dados em memória
pedidos = []
next_id = 1


@app.post("/pedidos", response_model=Pedido)
def criar_pedido(dados: PedidoCreate):
    """
    Cadastra novo pedido no banco de dados em memória
    """
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
    """
    Mostra pedidos cadastrados no banco de dados em memória
    """
    return pedidos


STATUS_VALIDOS = ["pendente", "pago", "enviado", "finalizado", "cancelado"]


@app.patch("/pedidos/{id}/status", response_model=Pedido)
def atualizar_status(id: int, status: str):
    """
    Para atualizar status dos pedidos para "pendente", "pago", "enviado", "finalizado", ou "cancelado" 
    """
    
    # Busca pedido
    pedido = next((p for p in pedidos if p.id == id), None)

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if status not in STATUS_VALIDOS:
        raise HTTPException(status_code=400, detail="Status inválido. Escreva: pendente, pago, enviado, finalizado, ou cancelado")

    pedido.status = status
   
    return pedido

