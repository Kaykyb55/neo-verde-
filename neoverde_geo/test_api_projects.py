"""
Teste simples da API de projetos
"""
import requests

try:
    # Testar API de projetos
    response = requests.get('http://localhost:5000/api/projects')
    
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type')}")
    print(f"\nResposta JSON:")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total de projetos retornados: {len(data) if isinstance(data, list) else 'N/A'}")
        
        if isinstance(data, list) and len(data) > 0:
            print(f"\nPrimeiro projeto:")
            print(f"  - ID: {data[0].get('id')}")
            print(f"  - Título: {data[0].get('title')}")
            print(f"  - Categoria: {data[0].get('category')}")
            print(f"  - Imagem: {data[0].get('image_url')}")
        else:
            print("Resposta:", data)
    else:
        print(f"Erro: {response.text}")
        
except Exception as e:
    print(f"Erro ao testar API: {e}")
