"""
Verificar estrutura da tabela media nos dois bancos
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
        
    print(f"\n{'='*60}")
    print(f"Banco: {db_path}")
    print('='*60)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Ver colunas da tabela media
        cursor.execute("PRAGMA table_info(media)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"Colunas existentes na tabela 'media':")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Contar mídias
        cursor.execute("SELECT COUNT(*) FROM media")
        count = cursor.fetchone()[0]
        print(f"\nTotal de mídias no banco: {count}")
        
        # Verificar colunas necessárias
        required_columns = ['views', 'likes_count', 'comments_count']
        missing_columns = [col for col in required_columns if col not in column_names]
        
        if missing_columns:
            print(f"\n⚠️ COLUNAS FALTANTES: {missing_columns}")
        else:
            print(f"\n✓ Todas as colunas necessárias estão presentes")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao verificar {db_path}: {e}")

print("\n" + "="*60)
