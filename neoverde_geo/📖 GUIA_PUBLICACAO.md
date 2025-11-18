# 📖 Guia Completo de Publicação do Site NeoVerde

## 🎯 Como Colocar o Site no Ar

---

## Opção 1: PythonAnywhere (GRATUITO e FÁCIL)

### Passo 1: Criar Conta
1. Acesse: https://www.pythonanywhere.com
2. Clique em "Start running Python online in less than a minute!"
3. Crie uma conta gratuita (Beginner Account)

### Passo 2: Upload dos Arquivos
1. Na dashboard, vá em "Files"
2. Clique em "Upload a file"
3. Faça upload de todos os arquivos do projeto:
   - `app.py`
   - `models.py`
   - `config.py`
   - Pasta `routes/`
   - Pasta `static/`
   - Pasta `templates/`
   - `requirements.txt`

### Passo 3: Instalar Dependências
1. Vá em "Consoles"
2. Clique em "Bash"
3. Execute:
```bash
pip3 install --user flask flask-sqlalchemy werkzeug
```

### Passo 4: Configurar Web App
1. Vá em "Web"
2. Clique em "Add a new web app"
3. Escolha "Flask"
4. Python version: 3.10
5. Path to your Flask app: `/home/seuusuario/app.py`

### Passo 5: Configurar Banco
1. No console Bash:
```bash
cd ~
python3 SETUP_FINAL_COMPLETO.py
```

### Passo 6: Recarregar
1. Vá em "Web"
2. Clique no botão verde "Reload"
3. Seu site está no ar! 
4. URL: `http://seuusuario.pythonanywhere.com`

---

## Opção 2: Heroku (RECOMENDADO)

### Passo 1: Preparar o Projeto

Crie os arquivos necessários:

**1. Procfile**
```
web: gunicorn app:app
```

**2. requirements.txt**
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Werkzeug==3.0.0
gunicorn==21.2.0
```

**3. runtime.txt**
```
python-3.11.0
```

### Passo 2: Instalar Heroku CLI
1. Baixe: https://devcenter.heroku.com/articles/heroku-cli
2. Instale no seu computador

### Passo 3: Fazer Deploy
```bash
# Login no Heroku
heroku login

# Criar app
heroku create neoverde-sustentavel

# Fazer deploy
git init
git add .
git commit -m "Deploy inicial"
git push heroku main

# Configurar banco
heroku run python SETUP_FINAL_COMPLETO.py
```

### Passo 4: Abrir o Site
```bash
heroku open
```

---

## Opção 3: Replit (MAIS FÁCIL)

### Passo 1: Criar Conta
1. Acesse: https://replit.com
2. Crie uma conta gratuita

### Passo 2: Criar Novo Repl
1. Clique em "+ Create Repl"
2. Template: "Python"
3. Nome: "neoverde-site"

### Passo 3: Upload dos Arquivos
1. Arraste todos os arquivos para o Replit
2. Ou use o botão de upload

### Passo 4: Configurar
No arquivo `.replit`, adicione:
```
run = "python app.py"
```

### Passo 5: Executar
1. Clique no botão "Run"
2. Seu site estará disponível em: `https://neoverde-site.seuusuario.repl.co`

---

## Opção 4: Vercel (PARA SITES ESTÁTICOS)

⚠️ **NOTA:** Vercel é melhor para sites estáticos. Para este projeto Flask, use PythonAnywhere ou Heroku.

---

## Opção 5: Servidor Próprio (VPS)

### Requisitos:
- Servidor Ubuntu 20.04+
- Python 3.8+
- Nginx
- Domínio próprio

### Passos:

**1. Conectar ao servidor**
```bash
ssh usuario@seu-servidor.com
```

**2. Instalar dependências**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

**3. Clonar projeto**
```bash
cd /var/www
sudo mkdir neoverde
cd neoverde
# Copiar arquivos do projeto aqui
```

**4. Criar ambiente virtual**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**5. Configurar Gunicorn**
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 app:app
```

**6. Configurar Nginx**
Criar arquivo `/etc/nginx/sites-available/neoverde`:
```nginx
server {
    listen 80;
    server_name seudominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /var/www/neoverde/static;
    }
}
```

**7. Ativar site**
```bash
sudo ln -s /etc/nginx/sites-available/neoverde /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

**8. Criar serviço systemd**
Criar arquivo `/etc/systemd/system/neoverde.service`:
```ini
[Unit]
Description=NeoVerde Flask App
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/neoverde
Environment="PATH=/var/www/neoverde/venv/bin"
ExecStart=/var/www/neoverde/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

**9. Iniciar serviço**
```bash
sudo systemctl start neoverde
sudo systemctl enable neoverde
```

---

## 🔒 Segurança IMPORTANTE

### Antes de publicar, MUDE:

**1. Senha do Admin**
```python
# No primeiro acesso, mude a senha de admin123
```

**2. Secret Key**
Em `config.py`:
```python
SECRET_KEY = 'sua-chave-secreta-super-forte-aqui'
```

**3. Modo Debug**
Em `app.py`:
```python
app.run(debug=False)  # MUITO IMPORTANTE!
```

---

## 📊 Monitoramento

### Logs do Heroku
```bash
heroku logs --tail
```

### Logs do PythonAnywhere
1. Vá em "Web"
2. Clique em "Log files"
3. Veja error.log e access.log

---

## 🌐 Domínio Personalizado

### Para conectar seu próprio domínio:

**PythonAnywhere:**
1. Vá em "Web"
2. Configure CNAME no seu provedor de domínio
3. Aponte para: `seuusuario.pythonanywhere.com`

**Heroku:**
```bash
heroku domains:add www.seudominio.com
```

**Configurar DNS:**
1. Acesse seu provedor de domínio (Registro.br, GoDaddy, etc)
2. Adicione CNAME:
   - Nome: www
   - Valor: [url-do-heroku-ou-pythonanywhere]

---

## ✅ Checklist Pré-Publicação

- [ ] Executei `SETUP_FINAL_COMPLETO.py`
- [ ] Testei localmente (http://localhost:5000)
- [ ] Mudei senha do admin
- [ ] Mudei SECRET_KEY
- [ ] Desabilitei DEBUG mode
- [ ] Criei requirements.txt
- [ ] Testei todas as páginas
- [ ] Testei admin panel
- [ ] Testei formulário de contato
- [ ] Testei em mobile (F12 > Device Toolbar)

---

## 🚨 Solução de Problemas Comuns

### Erro 500 no servidor
```
Causa: Banco de dados não criado
Solução: Execute SETUP_FINAL_COMPLETO.py no servidor
```

### Imagens não carregam
```
Causa: Path incorreto
Solução: Use URLs absolutas para imagens (https://...)
```

### Admin não funciona
```
Causa: JavaScript não carrega
Solução: Verifique F12 > Console para erros
```

---

## 📞 Suporte de Hospedagem

**PythonAnywhere:**
- Fórum: https://www.pythonanywhere.com/forums/
- Help: help@pythonanywhere.com

**Heroku:**
- Docs: https://devcenter.heroku.com
- Support: https://help.heroku.com

---

## 🎉 Pronto!

Seu site estará no ar e acessível para o mundo todo!

**URL de exemplo:**
- PythonAnywhere: `http://neoverde.pythonanywhere.com`
- Heroku: `https://neoverde-sustentavel.herokuapp.com`
- Replit: `https://neoverde-site.usuario.repl.co`

---

*Boa sorte com seu site! 🌿*
