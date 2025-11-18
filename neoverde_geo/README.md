# 🌿 NeoVerde Geografia

Sistema web desenvolvido em Flask para gestão de conteúdo geográfico com galeria de mídia, projetos, sistema de autenticação e painel administrativo.

## 📋 Índice

- [Características](#características)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Contribuindo](#contribuindo)

## ✨ Características

### Funcionalidades Principais

- 🔐 **Sistema de Autenticação**
  - Login local com email e senha
  - Login via Google OAuth 2.0
  - Sistema de permissões (admin/usuário regular)
  - Recuperação de senha (em desenvolvimento)

- 📸 **Galeria de Mídia**
  - Upload de imagens (PNG, JPG, JPEG, GIF, SVG)
  - Upload de vídeos (MP4, AVI, MOV)
  - Sistema de categorização
  - Curtidas e comentários
  - Limite de 50MB por arquivo

- 📁 **Gestão de Projetos**
  - Criação, edição e exclusão de projetos
  - Categorização de projetos
  - Associação com imagens

- 💬 **Sistema de Interação**
  - Comentários em mídias
  - Sistema de curtidas
  - Formulário de contato
  - Mensagens gerenciáveis pelo admin

- 🎛️ **Painel Administrativo**
  - Gerenciamento de usuários
  - Gerenciamento de mídia
  - Gerenciamento de projetos
  - Visualização de mensagens de contato
  - Estatísticas do sistema

## 🛠️ Tecnologias Utilizadas

### Backend
- **Flask 2.3.3** - Framework web
- **Flask-SQLAlchemy 3.0.5** - ORM para banco de dados
- **SQLite** - Banco de dados
- **Werkzeug 2.3.7** - Utilitários WSGI

### Autenticação
- **Google OAuth 2.0** - Autenticação via Google
- **google-auth 2.23.0**
- **google-auth-oauthlib 1.1.0**

### Segurança
- **Werkzeug Security** - Hash de senhas (PBKDF2-SHA256)
- **Python-dotenv 1.0.0** - Gerenciamento de variáveis de ambiente

## 📁 Estrutura do Projeto

```
neoverde_geo/
│
├── app.py                    # Aplicação principal (refatorada)
├── app_old.py               # Backup da versão anterior
├── config.py                # Configurações centralizadas
├── models.py                # Modelos de banco de dados
├── requirements.txt         # Dependências do projeto
├── .env.example            # Exemplo de variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
├── README.md               # Esta documentação
│
├── routes/                  # Módulo de rotas
│   ├── __init__.py         # Inicialização de blueprints
│   ├── main.py             # Rotas principais (index, admin)
│   ├── auth.py             # Rotas de autenticação
│   └── api.py              # Rotas da API REST
│
├── static/                  # Arquivos estáticos
│   ├── css/                # Estilos CSS
│   ├── js/                 # Scripts JavaScript
│   ├── images/             # Imagens do site
│   └── uploads/            # Uploads de usuários
│
├── templates/               # Templates HTML
│   ├── base.html           # Template base
│   ├── index_new.html      # Página inicial
│   ├── admin_new.html      # Painel administrativo
│   └── login_modern.html   # Página de login
│
└── instance/                # Dados da instância
    └── database.db         # Banco de dados SQLite
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional)

### Passos

1. **Clone ou baixe o repositório**

```bash
cd "site final de elsonn ja pra entrega/neoverde_geo"
```

2. **Crie um ambiente virtual (recomendado)**

```bash
python -m venv venv
```

3. **Ative o ambiente virtual**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instale as dependências**

```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

### 1. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

```env
# Chave secreta do Flask
SECRET_KEY=sua-chave-secreta-aqui

# Google OAuth (opcional)
GOOGLE_CLIENT_ID=seu-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=seu-google-client-secret

# Ambiente
FLASK_ENV=development
```

**⚠️ IMPORTANTE:** 
- Substitua `sua-chave-secreta-aqui` por uma string aleatória e complexa
- Para produção, use uma chave segura e única

### 2. Configurar Google OAuth (Opcional)

Se desejar usar login com Google:

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Ative a "Google+ API" ou "Google Identity Services"
4. Vá em "Credenciais" > "Criar credenciais" > "ID do cliente OAuth 2.0"
5. Configure a tela de consentimento OAuth
6. Adicione a URI de redirecionamento:
   - `http://localhost:5000/oauth2callback`
7. Copie o Client ID e Client Secret para o arquivo `.env`

### 3. Inicializar o Banco de Dados

O banco de dados será criado automaticamente ao executar a aplicação pela primeira vez.

## 🎮 Uso

### Iniciar o Servidor

```bash
python app.py
```

O servidor estará disponível em: **http://localhost:5000**

### Credenciais de Administrador Padrão

- **Email:** admin@neoverde.com
- **Senha:** admin123

**⚠️ IMPORTANTE:** Altere a senha após o primeiro login!

### Acessar o Sistema

1. **Página Inicial:** http://localhost:5000
2. **Login:** http://localhost:5000/login
3. **Painel Admin:** http://localhost:5000/admin (requer login como admin)

## 🔌 API Endpoints

### Autenticação

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/login` | Página de login |
| POST | `/login` | Processar login |
| POST | `/register` | Cadastrar usuário |
| GET | `/logout` | Fazer logout |
| GET | `/login/google` | Login via Google OAuth |

### Mídia

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/media` | Listar mídia |
| POST | `/api/media/upload` | Upload de arquivo |
| DELETE | `/api/media/<id>` | Deletar mídia |

### Projetos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/projects` | Listar projetos |
| POST | `/api/projects` | Criar projeto |
| PUT | `/api/projects/<id>` | Atualizar projeto |
| DELETE | `/api/projects/<id>` | Deletar projeto |

### Comentários

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/media/<id>/comments` | Listar comentários |
| POST | `/api/media/<id>/comments` | Adicionar comentário |
| DELETE | `/api/comments/<id>` | Deletar comentário |

### Curtidas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/media/<id>/like` | Curtir/descurtir |
| GET | `/api/media/<id>/liked` | Verificar curtida |

### Contato

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/contact` | Enviar mensagem |
| GET | `/api/contact/messages` | Listar mensagens (admin) |
| PUT | `/api/contact/messages/<id>/status` | Atualizar status |
| DELETE | `/api/contact/messages/<id>` | Deletar mensagem |

### Estatísticas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/stats/users` | Estatísticas de usuários |

## 🏗️ Arquitetura

### Padrão de Projeto

O projeto segue o padrão **Factory Pattern** com **Blueprints** do Flask:

- **Factory Pattern:** Função `create_app()` cria instâncias da aplicação
- **Blueprints:** Rotas organizadas em módulos lógicos
- **MVC Pattern:** Separação entre Models, Views (templates) e Controllers (rotas)

### Configurações

Três ambientes de configuração disponíveis:

- **Development:** Debug ativo, banco SQLite local
- **Production:** Debug desativado, HTTPS obrigatório para OAuth
- **Testing:** Ambiente isolado para testes

## 🔒 Segurança

### Medidas Implementadas

- ✅ Senhas hashadas com PBKDF2-SHA256
- ✅ Proteção CSRF (via Flask)
- ✅ Validação de tipos de arquivo
- ✅ Sanitização de nomes de arquivo
- ✅ Sistema de permissões (admin/usuário)
- ✅ Variáveis de ambiente para dados sensíveis
- ✅ `.gitignore` configurado para proteger `.env`

### Recomendações de Produção

1. Use HTTPS em produção
2. Configure `OAUTHLIB_INSECURE_TRANSPORT=0`
3. Use uma `SECRET_KEY` forte e única
4. Configure um banco de dados robusto (PostgreSQL/MySQL)
5. Implemente rate limiting
6. Configure backup automático do banco de dados
7. Use um servidor WSGI (Gunicorn, uWSGI)

## 🐛 Solução de Problemas

### Erro: "No such table"

Recrie o banco de dados:
```bash
rm instance/database.db
python app.py
```

### Erro: "Google OAuth não funciona"

1. Verifique se as credenciais estão corretas no `.env`
2. Confirme a URI de redirecionamento no Google Console
3. Certifique-se de que a API está ativada

### Erro: "Upload falha"

1. Verifique se a pasta `static/uploads` existe
2. Confirme as permissões de escrita
3. Verifique o tamanho do arquivo (máximo 50MB)

## 📝 Changelog

### Versão 2.0 (Atual) - Refatoração Completa

- ✨ Arquitetura modular com blueprints
- ✨ Configurações centralizadas
- ✨ Separação de modelos e rotas
- ✨ Factory pattern implementado
- ✨ Documentação completa em português
- 🗑️ Remoção de arquivos duplicados
- 🔧 Melhoria na organização do código

### Versão 1.0 - Versão Original

- ✅ Sistema de autenticação básico
- ✅ Galeria de mídia
- ✅ Sistema de projetos
- ✅ Painel administrativo

## 👥 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é de uso educacional e pode ser modificado conforme necessário.

## 📞 Suporte

Para dúvidas ou problemas:
- Email: admin@neoverde.com
- Crie uma issue no repositório

---

**Desenvolvido com 💚 para educação geográfica e sustentabilidade**
