# Apresentação técnica no GitHub

## Descrição curta

Agente de delivery com FastAPI, PostgreSQL, RAG, LangGraph e DeepSeek opcional.
Inclui segurança, observabilidade, avaliação, Streamlit, Docker e CI.

## Tópicos

python, fastapi, postgresql, deepseek, langgraph, rag, streamlit,
ai-engineering, generative-ai, pytest, docker, github-actions

## Roteiro para entrevista

1. Mostrar o fluxo Streamlit → FastAPI → LangGraph.
2. Consultar PED-001 e explicar SQL parametrizado e privilégio mínimo.
3. Perguntar sobre atraso e mostrar fontes recuperadas pelo RAG.
4. Tentar revelar o prompt e demonstrar o guardrail.
5. Simular cancelamento e comprovar que nenhuma ação foi executada.
6. Mostrar request ID, logs JSON, métricas e respostas 404/422/503.
7. Executar os testes e a avaliação.
8. Explicar fallback quando a DeepSeek não tem saldo ou está indisponível.
9. Abrir Docker, CI e documentação de deploy.
10. Discutir os limites técnicos com honestidade.

## Evidências

- 53 testes locais aprovados, incluindo integração PostgreSQL.
- 4/4 cenários de avaliação aprovados.
- RAG vetorial local com fontes.
- Grafo explícito com nós para segurança, pedido, política e ação sensível.
- Banco de testes separado e CI com PostgreSQL efêmero.
- Imagem Docker publicada pelo GitHub Actions após o push.

## Posicionamento

O projeto demonstra decisões de AI Engineering: integração de modelo com
fallback, grounding, ferramentas, orquestração, avaliação, segurança,
observabilidade e entrega. Dados, políticas e ações são fictícios.

Não possui vínculo oficial com o iFood e não é apresentado como produção.
