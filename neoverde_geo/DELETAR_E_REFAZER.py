"""
🔥 DELETAR E REFAZER AUTOMATICAMENTE (SEM PERGUNTAS)
"""
import os
import shutil

# Deletar banco
print("\n🔥 Deletando banco antigo...")
db_path = 'instance/database.db'
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print(f"✅ Deletado: {db_path}")
    except:
        print(f"❌ Erro ao deletar. FECHE O SERVIDOR primeiro!")
        exit(1)
else:
    print("✅ Nenhum banco encontrado")

# Criar pasta instance
os.makedirs('instance', exist_ok=True)

# Agora executa o script de refazer
print("\n🚀 Executando REFAZER_TUDO_DO_ZERO.py...\n")
os.system('py REFAZER_TUDO_DO_ZERO.py')
