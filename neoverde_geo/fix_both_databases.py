"""
Script para corrigir AMBOS os bancos de dados
"""
import sqlite3
import os

databases = [
    r'instance\database.db',
    r'..\instance\database.db'
]

for db_path in databases:
    if not os.path.exists(db_path):
        print(f"⚠️ Banco não encontrado: {db_path}")
        continue
        
    print(f"\n{'='*50}")
    print(f"Corrigindo: {db_path}")
    print('='*50)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Ver colunas atuais
        cursor.execute("PRAGMA table_info(project)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"Colunas existentes: {column_names}")
        
        # Adicionar colunas faltantes
        if 'likes_count' not in column_names:
            print("Adicionando coluna likes_count...")
            cursor.execute("ALTER TABLE project ADD COLUMN likes_count INTEGER DEFAULT 0")
            print("✓ Coluna likes_count adicionada!")
        else:
            print("✓ Coluna likes_count já existe")
            
        if 'views' not in column_names:
            print("Adicionando coluna views...")
            cursor.execute("ALTER TABLE project ADD COLUMN views INTEGER DEFAULT 0")
            print("✓ Coluna views adicionada!")
        else:
            print("✓ Coluna views já existe")
        
        # Contar projetos
        cursor.execute("SELECT COUNT(*) FROM project")
        count = cursor.fetchone()[0]
        print(f"Total de projetos no banco: {count}")
        
        conn.commit()
        conn.close()
        
        print(f"✅ {db_path} atualizado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao atualizar {db_path}: {e}")

print("\n" + "="*50)
print("AGORA REINICIE O SERVIDOR!")
print("="*50)
