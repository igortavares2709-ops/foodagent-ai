"""Logs estruturados e metricas simples em memoria."""

import json
import logging
from threading import Lock
from time import perf_counter
from uuid import uuid4

from fastapi import Request

_CONTADORES = {"requisicoes": 0, "erros": 0, "chats": 0}
_LOCK = Lock()
_LOGGER = logging.getLogger("foodagent")


def configurar_logs() -> None:
    if not _LOGGER.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        _LOGGER.addHandler(handler)
        _LOGGER.setLevel(logging.INFO)


def incrementar(chave: str) -> None:
    with _LOCK:
        _CONTADORES[chave] += 1


def metricas() -> dict[str, int]:
    with _LOCK:
        return dict(_CONTADORES)


async def middleware_observabilidade(request: Request, call_next):
    configurar_logs()
    request_id = request.headers.get("X-Request-ID") or uuid4().hex
    request.state.request_id = request_id
    inicio = perf_counter()
    incrementar("requisicoes")
    try:
        resposta = await call_next(request)
    except Exception:
        incrementar("erros")
        _LOGGER.exception(
            json.dumps(
                {
                    "event": "request_failed",
                    "request_id": request_id,
                    "path": request.url.path,
                },
                ensure_ascii=False,
            )
        )
        raise
    if resposta.status_code >= 500:
        incrementar("erros")
    resposta.headers["X-Request-ID"] = request_id
    _LOGGER.info(
        json.dumps(
            {
                "event": "request_completed",
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status": resposta.status_code,
                "duration_ms": round((perf_counter() - inicio) * 1000, 2),
            },
            ensure_ascii=False,
        )
    )
    return resposta
