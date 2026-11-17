import os

import httpx

from config import carregar_configuracao
from deepseek_client import ErroDeepSeek, consultar_deepseek


def main() -> None:
    try:
        carregar_configuracao()
        chave = os.getenv("DEEPSEEK_API_KEY", "").strip()

        if not chave:
            raise ValueError("DEEPSEEK_API_KEY não foi configurada no .env.")

        with httpx.Client() as cliente:
            resposta = consultar_deepseek(
                "Cumprimente o cliente em uma frase curta, em português.",
                chave,
                cliente=cliente,
            )
    except (ValueError, ErroDeepSeek) as erro:
        print(f"Não foi possível concluir: {erro}")
        raise SystemExit(1) from None

    print("Resposta da DeepSeek:")
    print(resposta)


if __name__ == "__main__":
    main()
