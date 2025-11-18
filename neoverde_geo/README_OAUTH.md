# 🔐 Configuração do Login com Google OAuth

Este guia vai te ajudar a configurar o login com Google no NeoVerde Sustentabilidade.

## 📋 Passo a Passo

### 1️⃣ Criar Projeto no Google Cloud Console

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Faça login com sua conta Google
3. Clique em **"Selecionar projeto"** → **"Novo projeto"**
4. Dê um nome ao projeto (ex: "NeoVerde Sustentabilidade")
5. Clique em **"Criar"**

### 2️⃣ Ativar APIs Necessárias

1. No menu lateral, vá em **"APIs e Serviços"** → **"Biblioteca"**
2. Procure por **"Google+ API"** ou **"Google Identity Services"**
3. Clique em **"Ativar"**

### 3️⃣ Configurar Tela de Consentimento OAuth

1. Vá em **"APIs e Serviços"** → **"Tela de consentimento OAuth"**
2. Selecione **"Externo"** (para testes) e clique em **"Criar"**
3. Preencha as informações:
   - **Nome do app:** NeoVerde Sustentabilidade
   - **E-mail de suporte:** seu.email@gmail.com
   - **Logotipo do app:** (opcional)
   - **Domínios autorizados:** localhost
   - **E-mail do desenvolvedor:** seu.email@gmail.com
4. Clique em **"Salvar e continuar"**
5. Em **"Escopos"**, clique em **"Adicionar ou remover escopos"**
6. Adicione os escopos:
   - `.../auth/userinfo.email`
   - `.../auth/userinfo.profile`
   - `openid`
7. Clique em **"Salvar e continuar"**
8. Em **"Usuários de teste"**, adicione seu e-mail
9. Clique em **"Salvar e continuar"**

### 4️⃣ Criar Credenciais OAuth

1. Vá em **"APIs e Serviços"** → **"Credenciais"**
2. Clique em **"+ Criar credenciais"** → **"ID do cliente OAuth 2.0"**
3. Selecione **"Aplicativo da Web"**
4. Configure:
   - **Nome:** NeoVerde Sustentabilidade Web Client
   - **URIs de redirecionamento autorizados:**
     ```
     http://localhost:5000/oauth2callback
     http://127.0.0.1:5000/oauth2callback
     ```
5. Clique em **"Criar"**
6. **IMPORTANTE:** Copie o **Client ID** e **Client Secret** que aparecem

### 5️⃣ Configurar no Projeto

1. Copie o arquivo `.env.example` para `.env`:
   ```bash
   copy .env.example .env
   ```

2. Abra o arquivo `.env` e cole suas credenciais:
   ```
   GOOGLE_CLIENT_ID=seu_client_id_aqui.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=seu_client_secret_aqui
   SECRET_KEY=uma_chave_secreta_aleatoria_aqui
   ```

3. **NUNCA compartilhe ou envie o arquivo `.env` para o Git!**

### 6️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

### 7️⃣ Executar o Servidor

```bash
python app.py
```

ou

```bash
py app.py
```

### 8️⃣ Testar o Login

1. Acesse: http://localhost:5000/login
2. Clique no botão **"Google"**
3. Você será redirecionado para a página de login do Google
4. Escolha sua conta Google
5. Autorize o aplicativo
6. Você será redirecionado de volta e estará logado!

## 🎯 Como Funciona

1. **Usuário clica em "Login com Google"**
2. **Aplicação redireciona para Google** (`/login/google`)
3. **Google autentica o usuário**
4. **Google redireciona de volta** (`/oauth2callback`)
5. **Aplicação recebe o token e cria/loga o usuário**
6. **Usuário é redirecionado para a página inicial ou admin**

## ⚠️ Solução de Problemas

### Erro: "redirect_uri_mismatch"
- Verifique se adicionou exatamente `http://localhost:5000/oauth2callback` nas URIs autorizadas
- Certifique-se de não ter espaços ou caracteres extras

### Erro: "invalid_client"
- Verifique se copiou corretamente o Client ID e Client Secret
- Confirme que as credenciais estão no arquivo `.env`

### Erro: "access_denied"
- Adicione seu e-mail nos "Usuários de teste" da tela de consentimento
- Certifique-se de que a aplicação está em modo de teste

### Login não funciona
- Verifique se instalou todas as dependências: `pip install -r requirements.txt`
- Confirme que o servidor está rodando
- Veja os logs do console para mensagens de erro

## 🔒 Segurança

- **NUNCA** compartilhe suas credenciais OAuth
- **NUNCA** envie o arquivo `.env` para o Git
- Em produção, use HTTPS (não HTTP)
- Altere a `SECRET_KEY` para uma string aleatória forte

## 📚 Recursos Adicionais

- [Documentação OAuth Google](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Melhores práticas OAuth](https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred)

## ✅ Pronto!

Agora seu site NeoVerde Sustentabilidade tem login com Google totalmente funcional! 🎉
