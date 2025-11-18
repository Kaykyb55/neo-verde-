# 🚀 Como Adicionar Projetos e Resolver o Erro 500

## 🔍 Problema Identificado

O erro **500 INTERNAL SERVER ERROR** acontece porque:
- O banco de dados não tem projetos cadastrados OU
- Há um problema na conexão com o banco de dados

## ✅ Solução Rápida

### Opção 1: Adicionar Projetos de Exemplo (RECOMENDADO)

1. **Pare o servidor** (Ctrl+C no terminal)

2. **Execute o script de projetos de exemplo**:
```powershell
python add_sample_projects.py
```

Isso vai adicionar 4 projetos lindos ao banco de dados:
- 🌳 Reflorestamento da Mata Atlântica
- ☀️ Energia Solar Comunitária  
- ♻️ Reciclagem e Educação Ambiental
- 💧 Preservação de Nascentes

3. **Inicie o servidor novamente**:
```powershell
python app.py
```

4. **Acesse o site** e veja os projetos funcionando!

### Opção 2: Verificar se o Banco Existe

Se ainda der erro, execute:

```powershell
python create_db.py
```

Depois execute a Opção 1 novamente.

### Opção 3: Adicionar Projetos Manualmente

1. Faça login como admin:
   - Email: `admin@neoverde.com`
   - Senha: `admin123`

2. Vá para o painel Admin

3. Adicione projetos manualmente com:
   - Título
   - Descrição
   - Categoria
   - Imagem (opcional)

## 🎯 O que foi Melhorado

✅ **Tratamento de erro na API** - Agora mostra mensagens claras
✅ **Script de projetos** - Adiciona 4 projetos bonitos automaticamente
✅ **Mensagens amigáveis** - Se der erro, você vê o que aconteceu
✅ **Logs no console** - Pode ver o que está acontecendo no F12

## 📱 Como Testar

Depois de adicionar os projetos:

1. Acesse `http://localhost:5000`
2. Clique em "Projetos Verdes" na sidebar
3. Você deve ver 4 cards lindos com projetos
4. Clique em qualquer card para ver o modal
5. Curta e comente!

## 🐛 Se Ainda Der Erro

Abra o console do navegador (F12) e veja:
- Console: Mensagens de erro do JavaScript
- Network: Veja a resposta da API /api/projects

Me mostre o que aparece e eu te ajudo! 🙋‍♂️
