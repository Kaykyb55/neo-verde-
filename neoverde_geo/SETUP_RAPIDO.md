# 🚀 Setup Rápido - NeoVerde Geografia

## Passo 1: Criar arquivo .env

Crie um arquivo chamado `.env` na pasta raiz do projeto com o seguinte conteúdo:

```env
# Chave secreta do Flask
SECRET_KEY=sk-ws-01-KZfMzzx8kUIt4YFUMJMlgtxc4Ck-1hQXGNV4YdUOmicUgU-9YuEFayAjnLCu9pvFfTE0yvReMujYcJMbqjNnwzQj2TTyWQ

# Google OAuth (opcional - deixe vazio se não for usar)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# Ambiente
FLASK_ENV=development
```

## Passo 2: Instalar dependências

```bash
pip install -r requirements.txt
```

## Passo 3: Executar a aplicação

```bash
python app.py
```

## Passo 4: Acessar o sistema

- **URL:** http://localhost:5000
- **Admin Email:** admin@neoverde.com
- **Admin Senha:** admin123

## ⚠️ IMPORTANTE

### Segurança da Chave

A chave fornecida (`sk-ws-01-KZfMzzx...`) foi configurada como SECRET_KEY da aplicação Flask. 

**ATENÇÃO:**
- Esta chave NÃO deve ser compartilhada publicamente
- Não faça commit do arquivo `.env` para o Git (já está no .gitignore)
- Para produção, considere gerar uma nova chave secreta

### Para gerar uma nova chave secreta (Python):

```python
import secrets
print(secrets.token_urlsafe(64))
```

## 📁 Estrutura do Projeto Organizada

```
neoverde_geo/
├── app.py              # Aplicação principal (refatorada)
├── config.py           # Configurações centralizadas
├── models.py           # Modelos de banco de dados
├── routes/             # Rotas organizadas em módulos
│   ├── main.py        # Rotas principais
│   ├── auth.py        # Autenticação
│   └── api.py         # API REST
├── templates/          # Templates HTML (limpos)
├── static/             # CSS, JS, imagens
└── .env               # Variáveis de ambiente (CRIAR)
```

## ✅ Melhorias Implementadas

1. **Arquitetura Modular** - Código organizado em módulos separados
2. **Configurações Centralizadas** - Todas as configs em `config.py`
3. **Blueprints** - Rotas separadas logicamente
4. **Factory Pattern** - Função `create_app()` para criar a aplicação
5. **Limpeza** - Arquivos duplicados removidos
6. **Documentação** - README completo em português

## 🆘 Problemas Comuns

### Erro ao criar .env

Se não conseguir criar o arquivo `.env` pelo editor, use o PowerShell:

```powershell
@"
SECRET_KEY=sk-ws-01-KZfMzzx8kUIt4YFUMJMlgtxc4Ck-1hQXGNV4YdUOmicUgU-9YuEFayAjnLCu9pvFfTE0yvReMujYcJMbqjNnwzQj2TTyWQ
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
FLASK_ENV=development
"@ | Out-File -FilePath .env -Encoding UTF8
```

### Módulos não encontrados

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Banco de dados com erro

```bash
rm instance/database.db
python app.py
```

---

**Pronto! Seu projeto está organizado e pronto para uso! 🎉**
