"""
Schemas Pydantic para validação de dados
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ProdutoInput(BaseModel):
    """
    Schema de entrada para cadastro de produto
    """

    nome: str = Field(..., min_length=3, description="Nome do produto")
    preco: float = Field(..., gt=0, description="Preço maior que zero")
    estoque: int = Field(..., ge=0, description="Estoque não-negativo")
    descricao: Optional[str] = Field(None, description="Descrição opcional")

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "Mouse Gamer",
                "preco": 129.90,
                "estoque": 50,
                "descricao": "RGB 16000 DPI",
            }
        }


class ProdutoOutput(BaseModel):
    """
    Schema de saída do cadastro
    """

    id: int
    nome: str
    preco: float
    status: str

# COM GPT

# Modelos
class Item(BaseModel):
    """
    Schema para cadastro de item
    """

    roupa: str = Field(..., min_length=3, description="Nome do produto/roupa")
    preco: float = Field(..., gt=0, description="Preço maior que zero")
    qtd: int = Field(..., gt=0, description="Quantidade maior que zero")

 
class PedidoCreate(BaseModel):
    """
    Schema para cadastro de pedido
    """

    cliente: str = Field(..., min_length=1, description="Nome do cliente")
    itens: List[Item]

    class Config:
        json_schema_extra = {
            "example": {
                "cliente": "Maria",
                "itens": [
                    {
                    "roupa": "saia",
                    "preco": 49.99,
                    "qtd": 2
                    }
                ]             
            }
        }
        
class Pedido(BaseModel):
    """
    Schema de saída do cadastro
    """

    id: int
    cliente: str
    itens: List[Item]
    total: float 
    status: str
    criadoEm: datetime



