# Avaliação, segurança e observabilidade

## Avaliação

`python avaliar.py` executa cenários de pedido, política, ação sensível e
injeção de prompt. A aprovação exige intenção, conteúdo e encaminhamento
esperados. Testes automatizados cobrem RAG, LangGraph, API e PostgreSQL.

## Segurança

- Dados e ações são fictícios.
- SQL usa parâmetros separados.
- O usuário PostgreSQL não é superusuário e tem apenas SELECT.
- `.env` e ambientes virtuais são ignorados.
- Padrões de email, telefone e CPF são mascarados.
- Tentativas simples de revelar prompt ou segredo são recusadas.
- Cancelamento e reembolso nunca são executados.
- Mensagens de erro não expõem conexão ou credenciais.

Essas medidas são defesa em profundidade inicial. Produção ainda exigiria
autenticação, autorização, rate limiting distribuído, secret manager, análise
de conteúdo e testes adversariais contínuos.

## Observabilidade

Cada requisição recebe `X-Request-ID`, preservando um valor enviado pelo
cliente ou gerando um UUID. Logs JSON registram método, rota, status e duração,
sem corpo da mensagem. `GET /metrics` expõe contadores em memória.

Os contadores reiniciam com o processo e não substituem Prometheus/OpenTelemetry
em ambientes com múltiplas réplicas.
