import httpx
import pytest

from deepseek_client import ErroDeepSeek, consultar_deepseek


def test_retorna_texto_da_resposta():
    def simular_api(request):
        assert request.url.path == "/chat/completions"
        return httpx.Response(
            200,
            json={
                "choices": [
                    {"message": {"content": "  Pedido fictício em preparo.  "}}
                ]
            },
        )

    with httpx.Client(transport=httpx.MockTransport(simular_api)) as cliente:
        resultado = consultar_deepseek(
            "Qual é o status do pedido?",
            "chave-ficticia",
            cliente=cliente,
        )

    assert resultado == "Pedido fictício em preparo."


@pytest.mark.parametrize(
    ("codigo", "mensagem"),
    [
        (401, "chave API foi recusada"),
        (402, "Saldo insuficiente"),
        (429, "Limite de requisições"),
        (500, "HTTP 500"),
    ],
)
def test_trata_erros_http(codigo, mensagem):
    transporte = httpx.MockTransport(
        lambda request: httpx.Response(codigo)
    )

    with httpx.Client(transport=transporte) as cliente:
        with pytest.raises(ErroDeepSeek, match=mensagem):
            consultar_deepseek(
                "Olá",
                "chave-ficticia",
                cliente=cliente,
            )


def test_trata_timeout():
    def simular_timeout(request):
        raise httpx.ReadTimeout("Timeout simulado", request=request)

    with httpx.Client(transport=httpx.MockTransport(simular_timeout)) as cliente:
        with pytest.raises(ErroDeepSeek, match="demorou"):
            consultar_deepseek(
                "Olá",
                "chave-ficticia",
                cliente=cliente,
            )


def test_rejeita_resposta_inesperada():
    transporte = httpx.MockTransport(
        lambda request: httpx.Response(200, json={"choices": []})
    )

    with httpx.Client(transport=transporte) as cliente:
        with pytest.raises(ErroDeepSeek, match="resposta inesperada"):
            consultar_deepseek(
                "Olá",
                "chave-ficticia",
                cliente=cliente,
            )


@pytest.mark.parametrize(
    ("mensagem", "chave"),
    [
        ("   ", "chave-ficticia"),
        ("Olá", "   "),
    ],
)
def test_rejeita_entrada_vazia_sem_chamar_api(mensagem, chave):
    def chamada_proibida(request):
        pytest.fail("Uma entrada inválida não deve chamar a API.")

    with httpx.Client(transport=httpx.MockTransport(chamada_proibida)) as cliente:
        with pytest.raises(ValueError):
            consultar_deepseek(mensagem, chave, cliente=cliente)