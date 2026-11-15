import httpx


class ErroDeepSeek(Exception):
    """Falha controlada na comunicação com a DeepSeek."""


def consultar_deepseek(
    mensagem: str,
    chave_api: str,
    *,
    cliente: httpx.Client,
) -> str:
    """Envia uma mensagem e retorna o texto da resposta."""
    mensagem = mensagem.strip()
    chave_api = chave_api.strip()

    if not mensagem:
        raise ValueError("A mensagem não pode estar vazia.")

    if not chave_api:
        raise ValueError("A chave da DeepSeek não está configurada.")

    try:
        resposta = cliente.post(
            "https://api.deepseek.com/chat/completions",
            headers={"Authorization": f"Bearer {chave_api}"},
            json={
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Você é um assistente de delivery em uma simulação. "
                            "Não afirme consultar ou alterar pedidos reais."
                        ),
                    },
                    {"role": "user", "content": mensagem},
                ],
                "max_tokens": 256,
                "stream": False,
            },
            timeout=20.0,
        )
        resposta.raise_for_status()
    except httpx.TimeoutException:
        raise ErroDeepSeek("A DeepSeek demorou para responder.") from None
    except httpx.HTTPStatusError as erro:
        mensagens = {
            401: "A chave API foi recusada.",
            402: "Saldo insuficiente na conta DeepSeek.",
            429: "Limite de requisições atingido. Tente mais tarde.",
        }
        codigo = erro.response.status_code
        aviso = mensagens.get(codigo, f"Falha na API DeepSeek: HTTP {codigo}.")
        raise ErroDeepSeek(aviso) from None
    except httpx.RequestError:
        raise ErroDeepSeek("Não foi possível conectar à DeepSeek.") from None

    try:
        texto = resposta.json()["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        raise ErroDeepSeek("A API retornou uma resposta inesperada.") from None

    if not isinstance(texto, str) or not texto.strip():
        raise ErroDeepSeek("A API retornou uma resposta sem texto.")

    return texto.strip()