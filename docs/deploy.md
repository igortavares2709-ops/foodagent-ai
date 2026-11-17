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

Deploy público validado em 17/11/2026:

- Interface: https://foodagent-ai-igortavares2709.onrender.com
- API/OpenAPI: https://foodagent-api-igortavares2709.onrender.com/docs
- Banco: PostgreSQL gerenciado, inicializado com dados fictícios.

O arquivo `render.yaml` documenta a infraestrutura da API, interface e banco.
A API usa variáveis de ambiente do Render; nenhuma credencial é versionada.
`DEEPSEEK_ENABLED=false` mantém a demonstração funcional com fallback local,
sem consumo de créditos.

A verificação de produção cobre `/health`, `/pedidos/PED-001`, `/chat` e
`/_stcore/health`. No plano gratuito, as instâncias podem dormir e o primeiro
acesso pode apresentar *cold start*. O banco gratuito também possui prazo de
expiração definido pela plataforma.

## Streamlit

A interface pode ser executada no mesmo docker-compose. Para hospedagem separada,
configure FOODAGENT_API_URL com a URL pública da API.

## Limites

O Blueprint prepara a infraestrutura, mas migrations automatizadas, domínio,
TLS customizado, autoscaling e gestão de segredos de produção exigem decisões
da plataforma e não devem ser simulados no portfólio.
