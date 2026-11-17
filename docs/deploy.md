# Deploy

O projeto inclui Dockerfile, docker-compose.yml e render.yaml.

## Validacao local com Docker

```powershell
docker compose up --build
```

- API: http://127.0.0.1:8000/docs
- Interface: http://127.0.0.1:8501

As credenciais do Compose são fictícias e exclusivas do ambiente local.

## Render

1. Faça fork ou use o repositório no GitHub.
2. No Render, escolha New > Blueprint.
3. Selecione o repositório e confirme o render.yaml.
4. Após o primeiro deploy, execute sql/003_docker_init.sql no banco gerenciado.
5. Configure DEEPSEEK_API_KEY como Secret somente quando houver créditos.

O deploy real depende de uma conta Render e pode gerar custos conforme o plano.
O endpoint /health verifica o processo; a consulta a /pedidos verifica o banco.

## Streamlit

A interface pode ser executada no mesmo docker-compose. Para hospedagem separada,
configure FOODAGENT_API_URL com a URL pública da API.

## Limites

O Blueprint prepara a infraestrutura, mas migrations automatizadas, domínio,
TLS customizado, autoscaling e gestão de segredos de produção exigem decisões
da plataforma e não devem ser simulados no portfólio.
