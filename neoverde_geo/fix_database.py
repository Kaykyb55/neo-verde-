"""
Script para corrigir e popular o banco de dados
"""
from app import create_app
from models import db, Project
from datetime import datetime

def fix_database():
    print("="*60)
    print("  CORRIGINDO BANCO DE DADOS")
    print("="*60)
    
    app = create_app()
    
    with app.app_context():
        # Criar todas as tabelas
        print("\n1. Criando estrutura do banco...")
        db.create_all()
        print("   ✓ Estrutura criada!")
        
        # Verificar projetos existentes
        print("\n2. Verificando projetos existentes...")
        existing = Project.query.count()
        print(f"   Projetos encontrados: {existing}")
        
        if existing == 0:
            print("\n3. Adicionando projetos de exemplo...")
            
            projects = [
                {
                    'title': 'Reflorestamento da Mata Atlântica',
                    'description': 'Projeto de recuperação de áreas degradadas da Mata Atlântica através do plantio de espécies nativas. Meta de 10.000 mudas plantadas até o final do ano.',
                    'category': 'Reflorestamento',
                    'image_url': 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=800'
                },
                {
                    'title': 'Energia Solar Comunitária',
                    'description': 'Instalação de painéis solares em comunidades carentes para promover o uso de energia limpa e reduzir custos com eletricidade.',
                    'category': 'Energia Renovável',
                    'image_url': 'https://images.unsplash.com/photo-1509391366360-2e959784a276?w=800'
                },
                {
                    'title': 'Reciclagem e Educação Ambiental',
                    'description': 'Programa de conscientização sobre reciclagem e separação de resíduos em escolas públicas, incluindo oficinas práticas e criação de hortas escolares.',
                    'category': 'Educação Ambiental',
                    'image_url': 'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=800'
                },
                {
                    'title': 'Preservação de Nascentes',
                    'description': 'Projeto de proteção e recuperação de nascentes em áreas rurais, garantindo água limpa para comunidades locais e preservando a biodiversidade.',
                    'category': 'Recursos Hídricos',
                    'image_url': 'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800'
                },
                {
                    'title': 'Horta Urbana Sustentável',
                    'description': 'Criação de hortas comunitárias em áreas urbanas, promovendo segurança alimentar e educação sobre agricultura orgânica.',
                    'category': 'Agricultura Sustentável',
                    'image_url': 'https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?w=800'
                },
                {
                    'title': 'Limpeza de Praias e Oceanos',
                    'description': 'Mutirões de limpeza de praias e conscientização sobre poluição marinha, com foco em redução de plásticos.',
                    'category': 'Preservação Marinha',
                    'image_url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800'
                }
            ]
            
            for i, proj_data in enumerate(projects, 1):
                project = Project(**proj_data)
                db.session.add(project)
                print(f"   {i}. {proj_data['title']}")
            
            db.session.commit()
            print(f"\n   ✓ {len(projects)} projetos adicionados!")
        else:
            print("\n   ✓ Banco já contém projetos!")
        
        # Listar todos os projetos
        print("\n4. Projetos no banco de dados:")
        all_projects = Project.query.all()
        for i, p in enumerate(all_projects, 1):
            print(f"   {i}. {p.title} ({p.category})")
        
        print("\n" + "="*60)
        print("  BANCO DE DADOS PRONTO! ✓")
        print("="*60)
        print("\n  Agora você pode:")
        print("  1. Iniciar o servidor: python app.py")
        print("  2. Acessar: http://localhost:5000")
        print("  3. Ver os projetos funcionando!\n")

if __name__ == '__main__':
    try:
        fix_database()
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\nSe o erro persistir, delete o arquivo 'database.db' e execute novamente.")
