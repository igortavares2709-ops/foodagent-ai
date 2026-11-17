"""Avaliacao local, deterministica e sem consumo de API."""

import json
from pathlib import Path

from agente import atender


def executar() -> dict[str, object]:
    casos = json.loads(
        (Path(__file__).parent / "evals" / "casos.json").read_text(encoding="utf-8")
    )
    resultados = []
    for caso in casos:
        saida = atender(caso["mensagem"], caso["pedido_id"])
        passou = (
            saida["intencao"] == caso["intencao"]
            and caso["contem"].casefold() in saida["resposta"].casefold()
            and saida.get("requer_humano", False) == caso["requer_humano"]
        )
        resultados.append({"nome": caso["nome"], "passou": passou})
    aprovados = sum(item["passou"] for item in resultados)
    return {
        "aprovados": aprovados,
        "total": len(resultados),
        "taxa": aprovados / len(resultados),
        "resultados": resultados,
    }


if __name__ == "__main__":
    print(json.dumps(executar(), ensure_ascii=False, indent=2))
