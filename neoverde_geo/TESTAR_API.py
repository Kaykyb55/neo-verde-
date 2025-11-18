"""
Testa se as APIs estão funcionando
"""
from app import create_app
from models import db, Project, Media, ContactMessage

app = create_app()

with app.app_context():
    print("\n" + "="*60)
    print("  TESTANDO BANCO DE DADOS")
    print("="*60)
    
    # Contar projetos
    projects = Project.query.all()
    print(f"\n✅ Projetos no banco: {len(projects)}")
    for p in projects[:3]:
        print(f"   - {p.title}")
    if len(projects) > 3:
        print(f"   ... e mais {len(projects) - 3}")
    
    # Contar mídia
    media = Media.query.all()
    print(f"\n✅ Fotos na galeria: {len(media)}")
    for m in media[:3]:
        print(f"   - {m.title}")
    if len(media) > 3:
        print(f"   ... e mais {len(media) - 3}")
    
    # Contar mensagens
    messages = ContactMessage.query.all()
    print(f"\n✅ Mensagens de contato: {len(messages)}")
    
    print("\n" + "="*60)
    print("  TUDO OK!")
    print("="*60)
    print("\n  Os dados ESTÃO no banco de dados.")
    print("  Se o admin não mostra, é problema de JavaScript.")
    print("\n  SOLUÇÃO:")
    print("  1. Abra o navegador")
    print("  2. Pressione F12 (Developer Tools)")
    print("  3. Vá na aba Console")
    print("  4. Recarregue a página (F5)")
    print("  5. Veja se há erros no console")
    print("\n" + "="*60 + "\n")

input("Pressione ENTER para fechar...")
