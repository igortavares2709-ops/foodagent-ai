# Testes com PostgreSQL

## Separacao dos ambientes

- `foodagent`: banco local da aplicacao; pedidos PED-001 e PED-002.
- `foodagent_test`: banco exclusivo dos testes; pedidos PED-901 e PED-902.
- `foodagent_app`: usuario sem superusuario, com SELECT na tabela pedidos.
- A API continua usando o banco definido em DB_NAME no ambiente local.
- Os testes alteram DB_NAME somente no processo Python e desfazem a alteracao ao terminar.

Nenhum teste de integracao grava, apaga ou recria tabelas. Os testes verificam
nome do banco, usuario e dados iniciais antes das consultas. DB_TEST_NAME diferente
de foodagent_test causa falha antes de abrir a conexao.

## Preparacao inicial no pgAdmin

1. Como postgres, criar foodagent_test, com owner postgres.
2. O usuario foodagent_app deve existir e ter uma senha local.
3. Abrir Query Tool conectado a foodagent_test como postgres.
4. Executar sql/002_preparar_banco_testes.sql.
5. Conferir PED-901 / em preparo e PED-902 / entregue.

O script recusa outro banco e pode ser reaplicado sem apagar dados.
Ele nao redefine pedidos ja existentes. Se a fixture estiver diferente, investigue
a alteracao; nao apague o banco da aplicacao para resolver um teste.

## Variaveis locais

O .env deve conter DB_HOST, DB_PORT, DB_NAME, DB_USER e DB_PASSWORD.
DB_TEST_NAME=foodagent_test e opcional; esse e o padrao dos testes.
Use a senha do foodagent_app, nunca a senha administrativa na aplicacao.
Nao envie .env, prints de senhas ou logs com credenciais.

## Comandos no PowerShell

Execute cada comando separadamente, na raiz do projeto.

Instalar dependencias:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Testes sem depender do banco (integracao fica explicitamente ignorada):

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Somente integracao, exigindo PostgreSQL disponivel:

```powershell
.\.venv\Scripts\python.exe -m pytest -q -m integration --integration
```

Suite completa:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --integration
```

Nao existe fallback silencioso para o banco da aplicacao. Se o banco de testes
nao estiver pronto, a execucao explicita de integracao falha.

## Cobertura da etapa

- Pedido persistido encontrado no repositorio.
- Pedido ausente retorna None.
- Entrada parecida com SQL e tratada como parametro.
- API consulta o PostgreSQL real sem substituir dependencias.
- Pedido ausente gera HTTP 404.
- Identificador invalido gera HTTP 422.
- Usuario da aplicacao tem leitura, sem escrita e sem superusuario.
- Guarda de seguranca rejeita nomes de bancos diferentes de foodagent_test.

## CI

.github/workflows/tests.yml executa a suite em Ubuntu, Python 3.14 e PostgreSQL 17.
As senhas visiveis no workflow sao ficticias e existem somente no contêiner
descartavel do job. Nao sao as senhas do computador do desenvolvedor.
Nenhum credito da DeepSeek e consumido.

O script scripts/preparar_ci.py so pode ser usado com CI=true; ele prepara o
banco efemero. Nao use essa ferramenta para administrar seu banco local.

## Limites conhecidos

A preparacao SQL e uma base inicial, nao um sistema completo de migrations.
A API abre uma conexao por consulta; pooling sera avaliado em uma etapa futura.
Integracao de escrita e rollback sera adicionada quando houver acoes persistidas.
