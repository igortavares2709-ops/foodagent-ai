# Case de produto — visão AI Builder

## Oportunidade

Atendimentos de delivery repetem perguntas sobre status, atraso, políticas e
cancelamento. A oportunidade é reduzir o esforço de triagem sem esconder
limites, inventar dados ou executar ações sensíveis automaticamente.

## Usuário e jornada

**Usuário principal:** cliente de um delivery fictício buscando uma resposta
rápida e compreensível.

1. O cliente descreve a necessidade em linguagem natural.
2. O agente identifica a intenção e consulta pedido ou política aplicável.
3. A resposta apresenta status, explicação e fontes.
4. Solicitações sensíveis viram simulação e seguem para revisão humana.
5. O request ID permite acompanhar o atendimento nos logs.

## Proposta de valor

- Responder dúvidas frequentes em uma única interface.
- Manter o atendimento disponível mesmo sem acesso ao provedor de LLM.
- Dar transparência por meio de fontes, estado do pedido e indicação de revisão.
- Evitar efeitos reais em uma demonstração de portfólio.

## Protótipo e automação

A experiência foi prototipada em Streamlit. FastAPI expõe o fluxo para outras
interfaces e integrações. LangGraph organiza as etapas do agente, o RAG recupera
políticas fictícias e o PostgreSQL fornece pedidos simulados.

O mesmo desenho pode ser conectado a fluxos de automação, como n8n, preservando
validação de entrada, idempotência e aprovação humana para ações de risco.

## Métricas de sucesso

| Sinal | Evidência atual |
|---|---|
| Confiabilidade funcional | 53 testes aprovados |
| Cobertura de cenários do agente | 4/4 avaliações aprovadas |
| Rastreabilidade | fontes e request ID nas respostas |
| Continuidade | fallback determinístico sem créditos de LLM |
| Segurança | prompt injection, PII e ações sensíveis testadas |

As métricas acima validam o protótipo; não representam redução real de custo ou
tempo de atendimento, pois o projeto não usa clientes nem operações reais.

## Decisões responsáveis

- Dados, pedidos, políticas e ações são fictícios.
- O agente não solicita senha, cartão, CPF ou chave de API.
- Cancelamento e reembolso exigem revisão humana.
- Logs não armazenam o texto das mensagens.
- Segredos ficam fora do Git e em variáveis de ambiente.

## Próximos experimentos

1. Medir taxa de resolução e tempo até resposta em um teste com usuários.
2. Comparar respostas com e sem RAG usando rubrica de precisão e utilidade.
3. Prototipar integração n8n para triagem e aprovação humana.
4. Testar acessibilidade e clareza da interface.
5. Criar painel de métricas de jornada e motivos de escalonamento.
