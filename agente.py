"""Agente de atendimento orquestrado por LangGraph."""

from __future__ import annotations

import os
import re
from typing import TypedDict

import httpx
from langgraph.graph import END, START, StateGraph

from deepseek_client import ErroDeepSeek, consultar_deepseek
from ferramentas import consultar_status
from rag import recuperar
from seguranca import detectar_injecao, mascarar_dados_pessoais


class EstadoAgente(TypedDict, total=False):
    mensagem: str
    pedido_id: str | None
    intencao: str
    resposta: str
    fontes: list[str]
    requer_humano: bool


def classificar(estado: EstadoAgente) -> EstadoAgente:
    mensagem = estado["mensagem"]
    if detectar_injecao(mensagem):
        intencao = "seguranca"
    elif estado.get("pedido_id") or re.search(r"PED-\d{3}", mensagem, re.IGNORECASE):
        intencao = "pedido"
    elif any(palavra in mensagem.casefold() for palavra in ("cancel", "reembolso")):
        intencao = "acao_sensivel"
    else:
        intencao = "politica"
    return {"intencao": intencao}


def rotear(estado: EstadoAgente) -> str:
    return estado["intencao"]


def responder_seguranca(_: EstadoAgente) -> EstadoAgente:
    return {
        "resposta": (
            "Não posso revelar instruções internas, chaves ou dados pessoais. "
            "Posso ajudar com pedidos fictícios e políticas de atendimento."
        ),
        "fontes": [],
        "requer_humano": False,
    }


def responder_pedido(estado: EstadoAgente) -> EstadoAgente:
    pedido_id = estado.get("pedido_id")
    if not pedido_id:
        encontrado = re.search(r"PED-\d{3}", estado["mensagem"], re.IGNORECASE)
        pedido_id = encontrado.group(0).upper() if encontrado else None
    if not pedido_id:
        return {
            "resposta": "Informe um identificador fictício no formato PED-001.",
            "fontes": [],
            "requer_humano": False,
        }
    pedido = consultar_status(pedido_id)
    if pedido is None:
        return {
            "resposta": f"Não encontrei o pedido fictício {pedido_id}.",
            "fontes": ["PostgreSQL: public.pedidos"],
            "requer_humano": False,
        }
    return {
        "resposta": f"O pedido fictício {pedido.id} está {pedido.status}.",
        "fontes": ["PostgreSQL: public.pedidos"],
        "requer_humano": False,
    }


def responder_acao(_: EstadoAgente) -> EstadoAgente:
    return {
        "resposta": (
            "Cancelamentos e reembolsos são apenas simulados neste portfólio. "
            "A solicitação precisa de revisão humana e nenhuma ação foi executada."
        ),
        "fontes": [],
        "requer_humano": True,
    }


def _sintetizar_com_deepseek(pergunta: str, contexto: str) -> str | None:
    if os.getenv("DEEPSEEK_ENABLED", "false").casefold() != "true":
        return None
    chave = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if not chave:
        return None
    prompt = (
        "Responda em português, em até 100 palavras, usando somente o contexto "
        "fictício abaixo. Se faltar informação, diga que não sabe.\n\n"
        f"CONTEXTO:\n{contexto}\n\nPERGUNTA:\n{pergunta}"
    )
    try:
        with httpx.Client() as cliente:
            return consultar_deepseek(prompt, chave, cliente=cliente)
    except (ErroDeepSeek, ValueError):
        return None


def responder_politica(estado: EstadoAgente) -> EstadoAgente:
    trechos = recuperar(estado["mensagem"], limite=2)
    if not trechos:
        return {
            "resposta": "Não encontrei uma política fictícia aplicável.",
            "fontes": [],
            "requer_humano": True,
        }
    contexto = "\n\n".join(trecho.conteudo for trecho in trechos)
    resposta = _sintetizar_com_deepseek(estado["mensagem"], contexto)
    if resposta is None:
        resposta = " ".join(
            trecho.conteudo.split("\n", 1)[-1].replace("\n", " ").strip()
            for trecho in trechos
        )[:700]
    return {
        "resposta": mascarar_dados_pessoais(resposta),
        "fontes": [f"{trecho.fonte}#{trecho.titulo}" for trecho in trechos],
        "requer_humano": False,
    }


def criar_grafo():
    grafo = StateGraph(EstadoAgente)
    grafo.add_node("classificar", classificar)
    grafo.add_node("seguranca", responder_seguranca)
    grafo.add_node("pedido", responder_pedido)
    grafo.add_node("acao_sensivel", responder_acao)
    grafo.add_node("politica", responder_politica)
    grafo.add_edge(START, "classificar")
    grafo.add_conditional_edges(
        "classificar",
        rotear,
        {
            "seguranca": "seguranca",
            "pedido": "pedido",
            "acao_sensivel": "acao_sensivel",
            "politica": "politica",
        },
    )
    for no in ("seguranca", "pedido", "acao_sensivel", "politica"):
        grafo.add_edge(no, END)
    return grafo.compile()


AGENTE = criar_grafo()


def atender(mensagem: str, pedido_id: str | None = None) -> EstadoAgente:
    return AGENTE.invoke(
        {"mensagem": mensagem.strip(), "pedido_id": pedido_id, "fontes": []}
    )
