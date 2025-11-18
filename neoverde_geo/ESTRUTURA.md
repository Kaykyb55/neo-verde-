# 📐 Estrutura do Projeto NeoVerde Geografia

## 🎯 Arquitetura Atual (Organizada e Centralizada)

```
neoverde_geo/
│
├── 📄 app.py                    # ⭐ Aplicação principal (Factory Pattern)
├── 📄 app_old.py               # 💾 Backup da versão anterior
├── 📄 config.py                # ⚙️ Configurações centralizadas
├── 📄 models.py                # 🗃️ Todos os modelos de dados
│
├── 📁 routes/                  # 🛣️ Módulo de rotas (Blueprints)
│   ├── __init__.py            # Inicializador de blueprints
│   ├── main.py                # Rotas principais (/, /admin)
│   ├── auth.py                # Autenticação (login, register, OAuth)
│   └── api.py                 # API REST (endpoints)
│
├── 📁 templates/               # 🎨 Templates HTML
│   ├── base.html              # Template base
│   ├── index_new.html         # Página inicial
│   ├── admin_new.html         # Painel administrativo
│   └── login_modern.html      # Página de login
│
├── 📁 static/                  # 🎭 Arquivos estáticos
│   ├── css/                   # Estilos CSS
│   ├── js/                    # Scripts JavaScript
│   ├── images/                # Imagens do site
│   └── uploads/               # 📤 Uploads de usuários
│
├── 📁 instance/                # 💿 Dados da aplicação
│   └── database.db            # Banco de dados SQLite
│
├── 📄 .env                     # 🔐 Variáveis de ambiente (CRIADO)
├── 📄 .env.example            # 📋 Exemplo de configuração
├── 📄 .gitignore              # 🚫 Arquivos ignorados
├── 📄 requirements.txt        # 📦 Dependências
├── 📄 README.md               # 📖 Documentação completa
├── 📄 SETUP_RAPIDO.md         # 🚀 Guia de instalação rápida
└── 📄 ESTRUTURA.md            # 📐 Este arquivo
```

## 🔄 Fluxo de Requisições

```
Cliente (Navegador)
        ↓
    app.py (Factory)
        ↓
    Blueprints (routes/)
        ├── main_bp   → Páginas principais
        ├── auth_bp   → Autenticação
        └── api_bp    → API REST
        ↓
    Models (models.py)
        ↓
    Database (SQLite)
```

## 🎯 Módulos e Responsabilidades

### 1. **app.py** - Aplicação Principal
- ✅ Factory Pattern (`create_app()`)
- ✅ Inicialização do banco de dados
- ✅ Registro de blueprints
- ✅ Criação de usuário admin
- ✅ Configuração de uploads

### 2. **config.py** - Configurações
- ✅ Classe `Config` base
- ✅ `DevelopmentConfig` - Desenvolvimento
- ✅ `ProductionConfig` - Produção
- ✅ `TestingConfig` - Testes
- ✅ Configurações OAuth Google
- ✅ Extensões de arquivo permitidas

### 3. **models.py** - Modelos de Dados
- ✅ `User` - Usuários do sistema
- ✅ `Media` - Galeria (imagens/vídeos)
- ✅ `Project` - Projetos
- ✅ `Comment` - Comentários
- ✅ `Like` - Curtidas
- ✅ `ContactMessage` - Mensagens de contato

### 4. **routes/** - Rotas (Blueprints)

#### 4.1 **main.py** - Rotas Principais
```python
GET  /           → Página inicial
GET  /admin      → Painel administrativo
```

#### 4.2 **auth.py** - Autenticação
```python
GET  /login              → Página de login
POST /login              → Processar login
POST /register           → Cadastrar usuário
GET  /logout             → Fazer logout
GET  /login/google       → OAuth Google
GET  /oauth2callback     → Callback OAuth
GET  /forgot-password    → Recuperação de senha
```

#### 4.3 **api.py** - API REST

**Mídia:**
```python
GET    /api/media              → Listar mídia
POST   /api/media/upload       → Upload de arquivo
DELETE /api/media/<id>         → Deletar mídia
```

**Projetos:**
```python
GET    /api/projects           → Listar projetos
POST   /api/projects           → Criar projeto
PUT    /api/projects/<id>      → Atualizar projeto
DELETE /api/projects/<id>      → Deletar projeto
```

**Comentários:**
```python
GET    /api/media/<id>/comments    → Listar comentários
POST   /api/media/<id>/comments    → Adicionar comentário
DELETE /api/comments/<id>          → Deletar comentário
```

**Curtidas:**
```python
POST   /api/media/<id>/like    → Curtir/descurtir
GET    /api/media/<id>/liked   → Verificar curtida
```

**Contato:**
```python
POST   /api/contact                      → Enviar mensagem
GET    /api/contact/messages             → Listar mensagens
PUT    /api/contact/messages/<id>/status → Atualizar status
DELETE /api/contact/messages/<id>        → Deletar mensagem
```

**Estatísticas:**
```python
GET    /api/stats/users        → Estatísticas de usuários
```

## 🔑 Relacionamentos do Banco de Dados

```
User (1) ────────────────────────┐
                                 │
Media (1) ──────────────── (N) Comment
   │
   └────────────────────── (N) Like

Project (independente)
ContactMessage (independente)
```

## 🎨 Melhorias Implementadas

### ✅ **Antes (Versão Antiga)**
- ❌ Tudo em um único arquivo (`app.py` com 593 linhas)
- ❌ Configurações espalhadas
- ❌ Rotas misturadas
- ❌ Arquivos de template duplicados
- ❌ Sem separação de responsabilidades

### ✅ **Depois (Versão Atual)**
- ✅ **Modular:** Código separado em módulos lógicos
- ✅ **Configurações Centralizadas:** Tudo em `config.py`
- ✅ **Blueprints:** Rotas organizadas por funcionalidade
- ✅ **Factory Pattern:** Criação flexível da aplicação
- ✅ **Templates Limpos:** Remoção de arquivos duplicados
- ✅ **Documentação Completa:** README, SETUP_RAPIDO, ESTRUTURA
- ✅ **Segurança:** Variáveis de ambiente (.env)

## 📊 Estatísticas do Projeto

| Componente | Arquivos | Linhas de Código (aprox.) |
|------------|----------|---------------------------|
| Configuração | 1 | ~70 |
| Modelos | 1 | ~170 |
| Rotas | 3 | ~400 |
| App Principal | 1 | ~90 |
| **Total Backend** | **6** | **~730** |
| Templates | 4 | ~1500 |
| Documentação | 3 | ~500 |

## 🚀 Como Funciona

### 1. Inicialização
```python
# app.py
app = create_app('development')
    ↓
config.py carrega configurações
    ↓
models.py inicializa banco de dados
    ↓
routes/ registra blueprints
```

### 2. Requisição HTTP
```
Cliente faz requisição → Flask recebe
    ↓
Blueprint identifica rota
    ↓
Função da rota processa
    ↓
Model acessa banco de dados (se necessário)
    ↓
Template renderizado
    ↓
Resposta enviada ao cliente
```

### 3. Autenticação
```
Login Form → auth.py → verifica senha
    ↓
Senha correta → Cria sessão
    ↓
Redireciona para admin (se admin) ou index
```

### 4. Upload de Mídia
```
Cliente envia arquivo → api.py
    ↓
Valida tipo de arquivo
    ↓
Salva em static/uploads/
    ↓
Cria registro no banco (Media)
    ↓
Retorna JSON com informações
```

## 🛡️ Segurança

- 🔐 Senhas hashadas (PBKDF2-SHA256)
- 🔐 Variáveis sensíveis em `.env`
- 🔐 `.env` no `.gitignore`
- 🔐 Validação de tipos de arquivo
- 🔐 Sanitização de nomes de arquivo
- 🔐 Sistema de permissões (admin/user)
- 🔐 CSRF protection (Flask)

## 🎯 Próximos Passos Sugeridos

1. **Testes Unitários** - Adicionar pasta `tests/`
2. **API Documentation** - Swagger/OpenAPI
3. **Cache** - Redis para performance
4. **Celery** - Tarefas assíncronas
5. **Docker** - Containerização
6. **CI/CD** - GitHub Actions
7. **Logging** - Sistema de logs estruturado
8. **Monitoring** - Prometheus/Grafana

---

**Estrutura organizada, código limpo, projeto profissional! 🎉**
