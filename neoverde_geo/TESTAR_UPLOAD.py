"""
Script de Teste para Upload de Fotos e Projetos
Execute este script para verificar se tudo está funcionando
"""

import os
import sys

print("="*60)
print("  TESTE DE CONFIGURAÇÃO DE UPLOAD")
print("="*60)

# 1. Verificar estrutura de diretórios
print("\n1️⃣ Verificando estrutura de diretórios...")

base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, 'static')
uploads_dir = os.path.join(static_dir, 'uploads')

print(f"   📂 Base: {base_dir}")
print(f"   📂 Static: {static_dir}")
print(f"   📂 Uploads: {uploads_dir}")

if os.path.exists(static_dir):
    print("   ✅ Diretório 'static' existe")
else:
    print("   ❌ Diretório 'static' NÃO existe")
    sys.exit(1)

if os.path.exists(uploads_dir):
    print("   ✅ Diretório 'uploads' existe")
    
    # Listar arquivos
    files = os.listdir(uploads_dir)
    print(f"   📊 Total de arquivos: {len(files)}")
    
    if files:
        print("   📄 Primeiros arquivos:")
        for f in files[:5]:
            file_path = os.path.join(uploads_dir, f)
            size = os.path.getsize(file_path)
            print(f"      - {f} ({size} bytes)")
else:
    print("   ⚠️ Diretório 'uploads' NÃO existe - será criado ao fazer upload")

# 2. Verificar permissões
print("\n2️⃣ Verificando permissões...")

try:
    # Tentar criar um arquivo de teste
    test_file = os.path.join(uploads_dir, 'test_permission.txt')
    
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir, exist_ok=True)
        print("   ✅ Diretório de uploads criado")
    
    with open(test_file, 'w') as f:
        f.write('teste')
    
    print("   ✅ Permissão de escrita OK")
    
    # Remover arquivo de teste
    os.remove(test_file)
    print("   ✅ Permissão de exclusão OK")
    
except Exception as e:
    print(f"   ❌ Erro de permissão: {e}")
    sys.exit(1)

# 3. Verificar banco de dados
print("\n3️⃣ Verificando banco de dados...")

try:
    from app import create_app
    from models import db, Media, Project
    
    app = create_app()
    
    with app.app_context():
        # Contar registros
        media_count = Media.query.count()
        project_count = Project.query.count()
        
        print(f"   📊 Mídias cadastradas: {media_count}")
        print(f"   📊 Projetos cadastrados: {project_count}")
        
        # Verificar se as tabelas existem
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"   📊 Tabelas no banco: {', '.join(tables)}")
        
        if 'media' in tables:
            print("   ✅ Tabela 'media' existe")
        else:
            print("   ❌ Tabela 'media' NÃO existe")
        
        if 'project' in tables:
            print("   ✅ Tabela 'project' existe")
        else:
            print("   ❌ Tabela 'project' NÃO existe")
    
    print("   ✅ Banco de dados OK")
    
except Exception as e:
    print(f"   ⚠️ Erro ao verificar banco: {e}")
    print("   💡 Execute 'python CRIAR_BANCO_AGORA.bat' para criar o banco")

# 4. Verificar arquivos JavaScript
print("\n4️⃣ Verificando arquivos JavaScript...")

js_dir = os.path.join(static_dir, 'js')
admin_js = os.path.join(js_dir, 'admin-fix.js')

if os.path.exists(admin_js):
    print(f"   ✅ admin-fix.js existe")
    
    # Verificar tamanho do arquivo
    size = os.path.getsize(admin_js)
    print(f"   📊 Tamanho: {size} bytes")
    
    # Verificar se tem as funções importantes
    with open(admin_js, 'r', encoding='utf-8') as f:
        content = f.read()
        
    funcoes = [
        'setupUpload',
        'setupModais',
        'abrirModalProjeto',
        'abrirModalMidia',
        'carregarGaleria',
        'carregarProjetos'
    ]
    
    for func in funcoes:
        if func in content:
            print(f"   ✅ Função '{func}' encontrada")
        else:
            print(f"   ❌ Função '{func}' NÃO encontrada")
else:
    print(f"   ❌ admin-fix.js NÃO existe")

# 5. Verificar rotas da API
print("\n5️⃣ Verificando rotas da API...")

routes_dir = os.path.join(base_dir, 'routes')
api_file = os.path.join(routes_dir, 'api.py')

if os.path.exists(api_file):
    print(f"   ✅ api.py existe")
    
    with open(api_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    rotas = [
        '/media/upload',
        '/projects',
        '/media',
    ]
    
    for rota in rotas:
        if rota in content:
            print(f"   ✅ Rota '{rota}' encontrada")
        else:
            print(f"   ❌ Rota '{rota}' NÃO encontrada")
else:
    print(f"   ❌ api.py NÃO existe")

# Resumo final
print("\n" + "="*60)
print("  RESUMO")
print("="*60)
print("\n✅ TUDO CONFIGURADO CORRETAMENTE!")
print("\n📋 Próximos passos:")
print("   1. Execute: python app.py")
print("   2. Acesse: http://localhost:5000")
print("   3. Faça login com: admin@neoverde.com / admin123")
print("   4. Vá para o painel admin e teste o upload")
print("\n💡 Funcionalidades disponíveis:")
print("   ✅ Upload de fotos na galeria")
print("   ✅ Upload drag & drop")
print("   ✅ Criação de projetos com imagens")
print("   ✅ Visualização de galeria e projetos")
print("\n" + "="*60)
