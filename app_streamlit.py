"""Interface demonstrativa do FoodAgent AI."""

import os

import httpx
import streamlit as st

API_URL = os.getenv("FOODAGENT_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="FoodAgent AI", page_icon="🍽️")
st.title("🍽️ FoodAgent AI")
st.caption("Portfólio independente com dados e ações fictícios.")

pedido_id = st.text_input("Pedido fictício (opcional)", placeholder="PED-001")
mensagem = st.text_area(
    "Como posso ajudar?",
    placeholder="Qual é o status do PED-001? ou Como funciona o cancelamento?",
)

if st.button("Enviar", type="primary", disabled=not mensagem.strip()):
    payload = {"mensagem": mensagem}
    if pedido_id.strip():
        payload["pedido_id"] = pedido_id.strip().upper()
    try:
        with httpx.Client(timeout=15) as cliente:
            resposta = cliente.post(f"{API_URL}/chat", json=payload)
            resposta.raise_for_status()
        dados = resposta.json()
        st.write(dados["resposta"])
        if dados["fontes"]:
            st.caption("Fontes: " + ", ".join(dados["fontes"]))
        if dados["requer_humano"]:
            st.warning("Este caso requer revisão humana.")
        st.caption("Request ID: " + dados["request_id"])
    except httpx.HTTPStatusError as erro:
        st.error(f"A API respondeu com erro {erro.response.status_code}.")
    except httpx.RequestError:
        st.error("Não foi possível acessar a API. Inicie o servidor FastAPI.")
