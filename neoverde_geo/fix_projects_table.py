"""
Script para adicionar colunas faltantes na tabela project
"""
from app import create_app
from models import db
import sqlite3

app = create_app()

with app.app_context():
    try:
        # Conectar ao banco de dados SQLite diretamente
        db_path = 'instance/database.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Verificando estrutura da tabela project...")
        
        # Ver colunas atuais
        cursor.execute("PRAGMA table_info(project)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"Colunas existentes: {column_names}")
        
        # Adicionar colunas faltantes se não existirem
        if 'likes_count' not in column_names:
            print("Adicionando coluna likes_count...")
            cursor.execute("ALTER TABLE project ADD COLUMN likes_count INTEGER DEFAULT 0")
            print("✓ Coluna likes_count adicionada!")
        else:
            print("Coluna likes_count já existe")
            
        if 'views' not in column_names:
            print("Adicionando coluna views...")
            cursor.execute("ALTER TABLE project ADD COLUMN views INTEGER DEFAULT 0")
            print("✓ Coluna views adicionada!")
        else:
            print("Coluna views já existe")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Banco de dados atualizado com sucesso!")
        print("Agora você pode acessar http://localhost:5000 e ver os projetos!")
        
    except Exception as e:
        print(f"❌ Erro ao atualizar banco: {e}")
        import traceback
        traceback.print_exc()
