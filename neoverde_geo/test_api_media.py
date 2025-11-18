"""
Teste simples da API de galeria/mídia
"""
import requests

try:
    # Testar API de mídia
    response = requests.get('http://localhost:5000/api/media')
    
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type')}")
    print(f"\nResposta JSON:")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total de mídias retornadas: {len(data) if isinstance(data, list) else 'N/A'}")
        
        if isinstance(data, list) and len(data) > 0:
            print(f"\nPrimeira mídia:")
            print(f"  - ID: {data[0].get('id')}")
            print(f"  - Título: {data[0].get('title')}")
            print(f"  - Tipo: {data[0].get('filetype')}")
            print(f"  - URL: {data[0].get('url')}")
        elif isinstance(data, list):
            print("Nenhuma mídia encontrada (lista vazia)")
        else:
            print("Resposta:", data)
    else:
        print(f"Erro: {response.text}")
        
except Exception as e:
    print(f"Erro ao testar API: {e}")
