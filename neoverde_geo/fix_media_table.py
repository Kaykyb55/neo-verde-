"""
Script para corrigir a tabela media em ambos os bancos de dados
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
    print(f"Corrigindo: {db_path}")
    print('='*60)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Ver colunas atuais
        cursor.execute("PRAGMA table_info(media)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"Colunas existentes: {column_names}")
        
        # Adicionar colunas faltantes
        changes_made = False
        
        if 'title' not in column_names:
            print("Adicionando coluna title...")
            cursor.execute("ALTER TABLE media ADD COLUMN title VARCHAR(200)")
            print("✓ Coluna title adicionada!")
            changes_made = True
        else:
            print("✓ Coluna title já existe")
        
        if 'likes_count' not in column_names:
            print("Adicionando coluna likes_count...")
            cursor.execute("ALTER TABLE media ADD COLUMN likes_count INTEGER DEFAULT 0")
            print("✓ Coluna likes_count adicionada!")
            changes_made = True
        else:
            print("✓ Coluna likes_count já existe")
            
        if 'views' not in column_names:
            print("Adicionando coluna views...")
            cursor.execute("ALTER TABLE media ADD COLUMN views INTEGER DEFAULT 0")
            print("✓ Coluna views adicionada!")
            changes_made = True
        else:
            print("✓ Coluna views já existe")
        
        if 'comments_count' not in column_names:
            print("Adicionando coluna comments_count...")
            cursor.execute("ALTER TABLE media ADD COLUMN comments_count INTEGER DEFAULT 0")
            print("✓ Coluna comments_count adicionada!")
            changes_made = True
        else:
            print("✓ Coluna comments_count já existe")
        
        if changes_made:
            conn.commit()
            print("✅ Mudanças aplicadas!")
        else:
            print("✅ Nenhuma mudança necessária")
        
        # Contar mídias
        cursor.execute("SELECT COUNT(*) FROM media")
        count = cursor.fetchone()[0]
        print(f"Total de mídias no banco: {count}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao atualizar {db_path}: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*60)
print("Agora vou copiar as mídias do banco completo...")
print("="*60)

# Copiar mídias do banco completo para o banco principal
source_db = r'instance\database.db'  # 14 mídias
target_db = r'..\instance\database.db'  # 0 mídias

try:
    conn_source = sqlite3.connect(source_db)
    conn_target = sqlite3.connect(target_db)
    
    cursor_source = conn_source.cursor()
    cursor_target = conn_target.cursor()
    
    # Limpar tabela de mídia no banco de destino
    print("\nLimpando mídias antigas do banco de destino...")
    cursor_target.execute("DELETE FROM media")
    cursor_target.execute("DELETE FROM comment")
    cursor_target.execute("DELETE FROM like")
    
    # Ver estrutura da tabela de origem
    cursor_source.execute("PRAGMA table_info(media)")
    columns_info = cursor_source.fetchall()
    column_names = [col[1] for col in columns_info]
    
    print(f"Colunas da tabela media: {column_names}")
    
    # Copiar mídias
    cursor_source.execute("SELECT * FROM media")
    medias = cursor_source.fetchall()
    
    print(f"Total de mídias a copiar: {len(medias)}")
    
    if len(medias) > 0:
        placeholders = ','.join(['?' for _ in column_names])
        insert_query = f"INSERT INTO media ({','.join(column_names)}) VALUES ({placeholders})"
        
        for media in medias:
            cursor_target.execute(insert_query, media)
            # media[1] é o filename
            print(f"  ✓ Copiado: {media[1]}")
        
        conn_target.commit()
        
        # Verificar
        cursor_target.execute("SELECT COUNT(*) FROM media")
        count = cursor_target.fetchone()[0]
        print(f"\n✅ Sucesso! Total de mídias no banco de destino: {count}")
    else:
        print("Nenhuma mídia para copiar")
    
    conn_source.close()
    conn_target.close()
    
except Exception as e:
    print(f"❌ Erro ao copiar mídias: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("PRONTO! Agora recarregue o site em http://localhost:5000")
print("A galeria deve aparecer!")
print("="*60)
