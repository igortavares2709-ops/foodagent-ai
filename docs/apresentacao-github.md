# Apresentacao no GitHub

## Nome sugerido

foodagent-ai

## Descricao curta

API de atendimento de delivery com FastAPI, PostgreSQL e cliente DeepSeek. Testes unitarios e de integracao, SQL parametrizado e CI. Portfolio de AI Engineering.

## Topicos sugeridos

python, fastapi, postgresql, deepseek, ai-engineering, portfolio, pytest, github-actions

## O que demonstrar em uma entrevista

1. Consultar PED-001 e explicar o fluxo HTTP -> dependencia -> repositorio -> PostgreSQL.
2. Mostrar as respostas 404, 422 e o teste de indisponibilidade 503.
3. Explicar SQL parametrizado, usuario sem superusuario e permissao SELECT.
4. Executar os 29 testes sem banco e os 7 testes reais no foodagent_test.
5. Mostrar a separacao entre credenciais locais e .env.example.
6. Explicar as decisoes e os limites antes de apresentar o roadmap.

## Estado real

A base de API e persistencia esta implementada. O cliente DeepSeek tem testes
simulados e tratamento de falhas; a resposta real ainda depende de saldo.
RAG, LangGraph, ferramentas de acoes, Streamlit e deploy sao etapas futuras.
O projeto e independente e nao possui vinculo oficial com o iFood.

Esta descricao evita apresentar funcionalidades planejadas como concluidas.
