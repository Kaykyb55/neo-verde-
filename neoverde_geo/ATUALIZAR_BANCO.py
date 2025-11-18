"""
Script para atualizar o banco de dados
Adiciona campo 'views' nas tabelas media e project
"""

import sqlite3
import os

# Caminho para o banco de dados
db_path = os.path.join('instance', 'database.db')

if not os.path.exists(db_path):
    print("❌ Banco de dados não encontrado!")
    exit(1)

print("🔧 Atualizando banco de dados...")

# Conectar ao banco
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Adicionar coluna views na tabela media
    print("📊 Adicionando campo 'views' na tabela media...")
    cursor.execute("ALTER TABLE media ADD COLUMN views INTEGER DEFAULT 0")
    print("✅ Campo 'views' adicionado em media!")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("⚠️ Campo 'views' já existe em media")
    else:
        print(f"❌ Erro em media: {e}")

try:
    # Adicionar coluna views na tabela project
    print("📊 Adicionando campo 'views' na tabela project...")
    cursor.execute("ALTER TABLE project ADD COLUMN views INTEGER DEFAULT 0")
    print("✅ Campo 'views' adicionado em project!")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("⚠️ Campo 'views' já existe em project")
    else:
        print(f"❌ Erro em project: {e}")

# Salvar mudanças
conn.commit()
conn.close()

print("\n✅ Banco de dados atualizado com sucesso!")
print("📌 Campo 'views' adicionado nas tabelas media e project")
print("🚀 Agora execute o servidor normalmente!")
