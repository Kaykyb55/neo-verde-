"""
Copiar os 13 projetos do banco neoverde_geo/instance/database.db
para o banco ..\instance\database.db que o servidor está usando
"""
import sqlite3

# Bancos de dados
source_db = r'instance\database.db'  # 13 projetos
target_db = r'..\instance\database.db'  # 2 projetos

print("Copiando projetos...")
print(f"Origem: {source_db}")
print(f"Destino: {target_db}")

try:
    # Conectar aos dois bancos
    conn_source = sqlite3.connect(source_db)
    conn_target = sqlite3.connect(target_db)
    
    cursor_source = conn_source.cursor()
    cursor_target = conn_target.cursor()
    
    # Limpar tabela de projetos no banco de destino
    print("\nLimpando projetos antigos do banco de destino...")
    cursor_target.execute("DELETE FROM project")
    cursor_target.execute("DELETE FROM project_comment")
    cursor_target.execute("DELETE FROM project_like")
    
    # Copiar projetos
    print("Copiando projetos...")
    cursor_source.execute("SELECT * FROM project")
    projects = cursor_source.fetchall()
    
    # Ver estrutura da tabela de origem
    cursor_source.execute("PRAGMA table_info(project)")
    columns_info = cursor_source.fetchall()
    column_names = [col[1] for col in columns_info]
    
    print(f"Colunas: {column_names}")
    print(f"Total de projetos a copiar: {len(projects)}")
    
    # Inserir projetos
    placeholders = ','.join(['?' for _ in column_names])
    insert_query = f"INSERT INTO project ({','.join(column_names)}) VALUES ({placeholders})"
    
    for project in projects:
        cursor_target.execute(insert_query, project)
        print(f"  ✓ Copiado: {project[1]}")  # project[1] é o título
    
    # Confirmar mudanças
    conn_target.commit()
    
    # Verificar
    cursor_target.execute("SELECT COUNT(*) FROM project")
    count = cursor_target.fetchone()[0]
    
    print(f"\n✅ Sucesso! Total de projetos no banco de destino: {count}")
    
    # Mostrar alguns projetos
    cursor_target.execute("SELECT id, title, category FROM project LIMIT 5")
    sample_projects = cursor_target.fetchall()
    print("\nPrimeiros 5 projetos:")
    for p in sample_projects:
        print(f"  - {p[1]} ({p[2]})")
    
    conn_source.close()
    conn_target.close()
    
    print("\n" + "="*50)
    print("AGORA ACESSE http://localhost:5000")
    print("Os projetos devem aparecer!")
    print("="*50)
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
