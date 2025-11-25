"""
Aplicação FastAPI principal
"""

from fastapi import FastAPI, HTTPException
from src.data.schemas import ProdutoInput, ProdutoOutput


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


@app.get("/item/{item_id}")
def get_item(item_id: int):
    """
    Busca item por ID
    """
    # Simulando base de dados
    items = {
        1: {"name": "Mouse", "price": 50.0},
        2: {"name": "Teclado", "price": 150.0},
        3: {"name": "Monitor", "price": 800.0},
    }

    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item {item_id} não encontrado")

    return items[item_id]


@app.post("/produtos", response_model=ProdutoOutput)
def criar_produto(produto: ProdutoInput):
    """
    Cadastra novo produto com validação
    """
    # Gera ID fake (em produção viria do banco)
    produto_id = 1

    # Define status baseado no estoque
    status = "disponível" if produto.estoque > 0 else "esgotado"

    return ProdutoOutput(
        id=produto_id, nome=produto.nome, preco=produto.preco, status=status
    )



