# 🌱 Site de Elson - NeoVerde Geografia

## 🚀 Como Executar o Site

### Método 1: Mais Rápido (Usando .bat)
1. Vá para a pasta `neoverde_geo`
2. Clique duas vezes no arquivo **`EXECUTAR.bat`** ou **`INICIAR_SERVIDOR.bat`**
3. Aguarde abrir o terminal
4. Acesse no navegador: **http://localhost:5000**

### Método 2: Pelo Terminal
1. Abra o PowerShell ou Prompt de Comando
2. Execute os comandos:
```powershell
cd "c:\Users\pesso\OneDrive\Desktop\site final de elsonn ja pra entrega\neoverde_geo"
python app.py
```
3. Acesse no navegador: **http://localhost:5000**

---

## 👤 Login de Administrador

Para acessar o painel de administração:
- **Email:** `admin@neoverde.com`
- **Senha:** `admin123`

---

## 📊 O que tem no site?

### ✅ Funcionalidades Principais:
- 🏠 **Dashboard** - Página inicial com estatísticas
- 🌱 **Projetos Verdes** - **13 projetos** de sustentabilidade
- 📸 **Galeria** - **14 fotos e vídeos**
- 💬 **Comentários** - Sistema de comentários nos projetos e galeria
- ❤️ **Curtidas** - Sistema de likes
- 📧 **Contato** - Formulário de contato
- 🔐 **Login/Registro** - Sistema de autenticação
- ⚙️ **Painel Admin** - Gerenciamento completo

---

## 🗂️ Estrutura do Projeto

```
neoverde_geo/
├── app.py                    # Arquivo principal
├── models.py                 # Banco de dados
├── config.py                 # Configurações
├── routes/                   # Rotas do site
│   ├── main.py              # Páginas principais
│   ├── auth.py              # Login/Registro
│   └── api.py               # API REST
├── templates/               # Páginas HTML
├── static/                  # CSS, JS, imagens
└── instance/                # Banco de dados SQLite
    └── database.db          # Dados do site
```

---

## 📝 Conteúdo do Site

### Projetos Cadastrados (13):
1. 🌳 Reflorestamento Mata Atlântica
2. ☀️ Energia Solar Comunitária
3. 🏫 Programa Escola Sustentável
4. 💧 Proteção de Nascentes
5. 🌱 Hortas Urbanas Orgânicas
6. 🌊 Limpeza Oceanos e Praias
7. 🏢 Telhados Verdes Urbanos
8. 🚴 Mobilidade Verde
9. 🐝 Proteção de Polinizadores
10. 🌲 Bosques Nativos Urbanos
11. 🌾 Agricultura Regenerativa
12. ⚡ Eficiência Energética
13. (+ 1 projeto de teste)

### Galeria (14 itens):
- 12 imagens sobre sustentabilidade
- 1 vídeo
- 1 imagem adicional

---

## 🛑 Como Parar o Servidor

- Pressione **Ctrl + C** no terminal onde o servidor está rodando

---

## ⚠️ Problemas Comuns

### "Python não foi encontrado"
- Certifique-se de que o Python está instalado
- Ou use os arquivos .bat que já estão configurados

### "Porta 5000 já está em uso"
- Pare o servidor anterior (Ctrl+C)
- Ou mude a porta no arquivo `app.py`

### "Projetos não aparecem"
- O banco de dados já está configurado com 13 projetos
- Recarregue a página (F5)

---

## 🎯 Tecnologias Utilizadas

- **Backend:** Python + Flask
- **Banco de Dados:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript
- **Autenticação:** Flask Sessions + OAuth Google
- **Estilo:** CSS customizado com animações

---

## 📞 Informações Adicionais

**Status:** ✅ Pronto para entrega  
**Projetos:** 13 cadastrados  
**Galeria:** 14 mídias  
**Usuário Admin:** Configurado  
**Banco de Dados:** Sincronizado  

---

**Desenvolvido para o projeto de Geografia - 2025** 🌍
