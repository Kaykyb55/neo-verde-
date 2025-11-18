"""
Testa se a API está respondendo corretamente
"""
import requests

print("\n" + "="*60)
print("  TESTANDO API")
print("="*60)

# Testar API de projetos
print("\n1. Testando /api/projects...")
try:
    r = requests.get('http://localhost:5000/api/projects', timeout=5)
    if r.status_code == 200:
        projects = r.json()
        print(f"   ✅ API funcionando! {len(projects)} projetos encontrados")
        for p in projects[:3]:
            print(f"      - {p['title']}")
    else:
        print(f"   ❌ Erro: Status {r.status_code}")
        print(f"   Resposta: {r.text}")
except requests.exceptions.ConnectionError:
    print("   ❌ SERVIDOR NÃO ESTÁ RODANDO!")
    print("   Execute: INICIAR_SERVIDOR.bat")
except Exception as e:
    print(f"   ❌ Erro: {str(e)}")

# Testar API de mídia
print("\n2. Testando /api/media...")
try:
    r = requests.get('http://localhost:5000/api/media', timeout=5)
    if r.status_code == 200:
        media = r.json()
        print(f"   ✅ API funcionando! {len(media)} fotos encontradas")
    else:
        print(f"   ❌ Erro: Status {r.status_code}")
except requests.exceptions.ConnectionError:
    print("   ❌ SERVIDOR NÃO ESTÁ RODANDO!")
except Exception as e:
    print(f"   ❌ Erro: {str(e)}")

print("\n" + "="*60)
print("  FIM DO TESTE")
print("="*60 + "\n")

input("Pressione ENTER...")
