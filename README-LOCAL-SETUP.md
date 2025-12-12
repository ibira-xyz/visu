# Setup Local com Docker (Espelhando Produção)

Este documento descreve como executar o projeto localmente usando containers Docker da mesma forma que em produção.

## 🏗️ Arquitetura

**Produção:**
- API Gateway AWS → Lambda Functions (containerizadas)
- Rotas: `/` e `/post/{slug}`

**Local:**
- Nginx (simula API Gateway) → Lambda Containers com RIE
- Mesmos handlers e Dockerfile de produção

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Make (opcional, mas recomendado)

## 🚀 Como Usar

### Opção 1: Usando Make (Recomendado)

```bash
# Ver comandos disponíveis
make help

# Construir e iniciar os serviços
make build
make up

# Ou tudo de uma vez
make rebuild

# Ver logs
make logs

# Testar as Lambdas diretamente
make test-index
make test-post

# Testar através do Nginx (stack completo)
make test-nginx

# Parar os serviços
make down
```

### Opção 2: Usando Docker Compose diretamente

```bash
# Construir as imagens
docker-compose build

# Iniciar os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar os serviços
docker-compose down
```

## 🌐 Acessando a Aplicação

Após iniciar os serviços:

- **Aplicação completa:** http://localhost:8080
- **Index/Home:** http://localhost:8080/
- **Post individual:** http://localhost:8080/post/{slug}
- **Arquivos estáticos:** http://localhost:8080/static/...

### Testando Lambdas Diretamente (sem Nginx)

```bash
# Lambda Index (porta 9000)
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

# Lambda Post (porta 9001)
curl -XPOST "http://localhost:9001/2015-03-31/functions/function/invocations" \
  -d '{"pathParameters":{"slug":"seu-slug"}}'
```

## 📁 Estrutura de Arquivos

```
visu/
├── docker-compose.yml          # Orquestração dos serviços
├── Makefile                    # Comandos facilitadores
├── nginx/
│   └── nginx.conf             # Configuração do proxy (simula API Gateway)
└── src/
    ├── Dockerfile             # Mesmo Dockerfile de produção
    ├── config/
    │   └── local.yaml         # Config para ambiente local
    └── lambda_handlers/
        ├── lambda_index.py    # Handler da rota /
        └── lambda_post.py     # Handler da rota /post/{slug}
```

## 🔄 Alternativas de Routing Local

### 1. **Nginx (Implementado)** ✅
- ✅ Simples e leve
- ✅ Próximo ao comportamento do API Gateway
- ✅ Serve arquivos estáticos
- ❌ Não simula todas features do API Gateway

### 2. **LocalStack**
```bash
# Instalar LocalStack
pip install localstack

# Iniciar
localstack start

# Configurar API Gateway completo
# (mais complexo, mas 100% compatível com AWS)
```

### 3. **AWS SAM Local**
```bash
# Instalar SAM CLI
brew install aws-sam-cli

# Criar template.yaml e executar
sam local start-api
```

### 4. **Apenas Lambda RIE** (mais simples)
```bash
# Executar uma Lambda diretamente
docker run -p 9000:8080 lambda-index:latest

# Invocar
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

## 🐛 Troubleshooting

### Logs não aparecem
```bash
docker-compose logs -f lambda-index
docker-compose logs -f lambda-post
docker-compose logs -f nginx
```

### Porta já em uso
Edite `docker-compose.yml` e mude as portas:
```yaml
ports:
  - "8081:80"  # Era 8080:80
```

### Rebuild forçado
```bash
docker-compose build --no-cache
docker-compose up -d --force-recreate
```

### Verificar se containers estão rodando
```bash
docker-compose ps
```

## 🔧 Configuração

### Variáveis de Ambiente

Edite `docker-compose.yml` para ajustar variáveis:

```yaml
environment:
  - AWS_REGION=us-east-1
  - CUSTOM_VAR=value
```

### Configuração da Aplicação

Edite `src/config/local.yaml` para configurações específicas do ambiente local.

## 📊 Diferenças vs Flask Local

| Aspecto | Flask (`local_server.py`) | Docker + Lambda |
|---------|---------------------------|-----------------|
| Ambiente | Python local | Container isolado |
| Código | Rotas Flask | Handlers Lambda |
| Hot reload | ✅ Sim | ❌ Não (rebuild necessário) |
| Produção | ❌ Diferente | ✅ Idêntico |
| Setup | Rápido | Mais complexo |
| Debugging | Fácil | Requer logs |

## 💡 Recomendações

- **Desenvolvimento rápido:** Use `local_server.py` (Flask)
- **Testes pré-deploy:** Use Docker (esta configuração)
- **CI/CD:** Use mesmas imagens Docker

## 📚 Próximos Passos

1. Adicionar health checks no `docker-compose.yml`
2. Configurar volumes para desenvolvimento com hot reload
3. Adicionar testes automatizados
4. Integrar com LocalStack para simular S3, DynamoDB, etc.
