# 🌿 Sistema NeoVerde - Sustentabilidade é Vida

## 📋 Sistema Completo de Gestão Ambiental

Sistema web completo para gerenciamento de projetos de sustentabilidade, galeria de fotos, comentários, curtidas e muito mais!

---

## ✨ Funcionalidades Implementadas

### 🌐 Site Principal
- ✅ **Dashboard** - Estatísticas em tempo real
- ✅ **12 Projetos de Sustentabilidade** completos com:
  - Descrições detalhadas
  - Imagens em alta qualidade
  - Sistema de curtidas
  - Comentários
  - Modal de visualização completa
- ✅ **12 Fotos na Galeria** com:
  - Visualização em grid responsivo
  - Modal fullscreen
  - Curtidas e comentários
  - Categorias organizadas
- ✅ **Formulário de Contato** funcional
- ✅ **Seção Sobre** limpa e organizada
- ✅ **Design Moderno** e responsivo

### 👨‍💼 Painel Administrativo
- ✅ **Dashboard Admin** com estatísticas completas
- ✅ **Gerenciamento de Projetos**
  - Listar todos os projetos
  - Ver detalhes
  - Excluir projetos
- ✅ **Gerenciamento de Galeria**
  - Ver todas as fotos
  - Estatísticas de curtidas/comentários
  - Excluir mídias
- ✅ **Mensagens de Contato**
  - Ver todas as mensagens
  - Marcar como lida
  - Excluir mensagens
- ✅ **Interface moderna** e intuitiva

---

## 🚀 Como Iniciar o Sistema

### Método 1: Arquivo .bat (RECOMENDADO)

**1. Configure o banco de dados:**
```
Clique 2x em: SETUP_FINAL_COMPLETO.bat
```

**2. Inicie o servidor:**
```
Clique 2x em: INICIAR_SERVIDOR.bat
```

**3. Acesse no navegador:**
```
http://localhost:5000
```

### Método 2: Linha de Comando

```bash
# 1. Configurar banco
python SETUP_FINAL_COMPLETO.py

# 2. Iniciar servidor
python app.py

# 3. Acessar
http://localhost:5000
```

---

## 🔐 Credenciais de Acesso

### Administrador
```
Email: admin@neoverde.com
Senha: admin123
```

### Usuários de Teste
```
João Silva: joao@exemplo.com / senha123
Maria Santos: maria@exemplo.com / senha123
Pedro Oliveira: pedro@exemplo.com / senha123
```

---

## 📊 Conteúdo do Sistema

### 12 Projetos Incluídos:

1. 🌳 **Reflorestamento da Mata Atlântica** - 500 hectares, 50.000 mudas
2. ☀️ **Energia Solar Comunitária** - 200 residências, 95% economia
3. ♻️ **Programa Escola Sustentável** - 50 escolas, 5.000 alunos
4. 💧 **Proteção de Nascentes** - 30 nascentes protegidas
5. 🥬 **Hortas Urbanas Orgânicas** - 100 hortas, 300 famílias
6. 🌊 **Limpeza de Oceanos e Praias** - 15 ton/ano de resíduos
7. 🌿 **Telhados Verdes Urbanos** - 50 telhados, 5°C mais fresco
8. 🚴 **Mobilidade Verde** - 30km ciclovias, 20 estações
9. 🐝 **Proteção de Polinizadores** - 10.000 flores nativas
10. 🌲 **Bosques Nativos Urbanos** - 10 bosques, 5.000 árvores
11. 🌾 **Agricultura Regenerativa** - 50 propriedades rurais
12. 💡 **Eficiência Energética** - 40% economia energia

### 12 Fotos Profissionais:

- Floresta Atlântica Preservada
- Energia Solar Residencial
- Centro de Reciclagem
- Nascente Protegida
- Horta Comunitária
- Praia Preservada
- Parque Eólico
- Polinizadores em Ação
- Educação Ambiental
- Compostagem Doméstica
- Mobilidade Sustentável
- Telhado Verde Urbano

---

## 🎨 Tecnologias Utilizadas

### Backend
- **Python 3.x**
- **Flask** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados
- **Werkzeug** - Segurança e hashing

### Frontend
- **HTML5** - Estrutura
- **CSS3** - Estilização moderna
- **JavaScript ES6+** - Interatividade
- **Font Awesome** - Ícones
- **Google Fonts** - Tipografia

### Recursos
- **Design Responsivo** - Mobile, tablet e desktop
- **Modais Dinâmicos** - Para projetos e galeria
- **API RESTful** - Comunicação assíncrona
- **Sistema de Autenticação** - Login seguro
- **CRUD Completo** - Create, Read, Update, Delete

---

## 📁 Estrutura do Projeto

```
neoverde_geo/
├── app.py                      # Aplicação principal
├── models.py                   # Modelos do banco de dados
├── config.py                   # Configurações
├── routes/
│   ├── main.py                 # Rotas principais
│   ├── auth.py                 # Autenticação
│   └── api.py                  # API REST
├── static/
│   ├── css/
│   │   ├── modern-style.css    # Estilos principais
│   │   └── modern-admin.css    # Estilos admin
│   └── js/
│       ├── modern-main.js      # JavaScript principal
│       └── modern-admin.js     # JavaScript admin
├── templates/
│   ├── index_new.html          # Página principal
│   ├── admin_new.html          # Painel admin
│   └── login_modern.html       # Página de login
└── instance/
    └── database.db             # Banco de dados SQLite
```

---

## 🔧 Arquivos Importantes

### Configuração e Setup
- `SETUP_FINAL_COMPLETO.py` - **Configuração completa** do sistema
- `SETUP_FINAL_COMPLETO.bat` - Executa setup (Windows)
- `INICIAR_SERVIDOR.bat` - Inicia o servidor
- `TESTAR.bat` - Testa o banco de dados

### Documentação
- `🎯 README - LEIA PRIMEIRO.md` - Este arquivo
- `📖 GUIA_PUBLICACAO.md` - Como publicar o site
- `✅ CHECKLIST_FINAL.md` - Lista de verificação

---

## ✅ Checklist de Funcionalidades

### Site Principal
- [x] Dashboard com estatísticas
- [x] 12 Projetos completos
- [x] 12 Fotos na galeria
- [x] Sistema de curtidas (projetos e fotos)
- [x] Sistema de comentários (projetos e fotos)
- [x] Modais de visualização
- [x] Formulário de contato
- [x] Design responsivo
- [x] Animações suaves
- [x] SEO otimizado

### Painel Admin
- [x] Dashboard administrativo
- [x] Listagem de projetos
- [x] Listagem de mídias
- [x] Gerenciamento de mensagens
- [x] Estatísticas em tempo real
- [x] Sistema de autenticação
- [x] Interface intuitiva

### Backend
- [x] API RESTful completa
- [x] Banco de dados SQLite
- [x] Autenticação segura
- [x] CRUD de projetos
- [x] CRUD de mídias
- [x] Sistema de comentários
- [x] Sistema de curtidas
- [x] Mensagens de contato

---

## 🌐 Como Publicar o Site

Veja o arquivo `📖 GUIA_PUBLICACAO.md` para instruções detalhadas de como colocar o site no ar!

---

## 🐛 Solução de Problemas

### Servidor não inicia
```bash
# Verifique se a porta 5000 está livre
netstat -ano | findstr :5000

# Se estiver ocupada, mate o processo:
taskkill /PID [número_do_PID] /F
```

### Banco de dados não carrega
```bash
# Execute novamente o setup
python SETUP_FINAL_COMPLETO.py
```

### Admin zerado
1. Abra F12 no navegador
2. Vá na aba Console
3. Procure por erros em vermelho
4. Se houver erro, limpe o cache (Ctrl+Shift+R)

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique o `✅ CHECKLIST_FINAL.md`
2. Consulte o `📖 GUIA_PUBLICACAO.md`
3. Execute `TESTAR.bat` para verificar o banco

---

## 📜 Licença

Sistema desenvolvido para NeoVerde Geografia - Todos os direitos reservados.

---

## 🎉 Status do Projeto

**✅ SISTEMA 100% COMPLETO E PRONTO PARA USO!**

- ✅ 12 Projetos cadastrados
- ✅ 12 Fotos na galeria
- ✅ Sistema de comentários funcionando
- ✅ Sistema de curtidas funcionando
- ✅ Painel admin completo
- ✅ Design moderno e responsivo
- ✅ Código organizado e documentado

**O SITE ESTÁ PRONTO PARA SER PUBLICADO! 🚀**

---

*Desenvolvido com 💚 por NeoVerde - Sustentabilidade é Vida*
