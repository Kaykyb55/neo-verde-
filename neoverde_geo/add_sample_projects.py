"""
Script para adicionar projetos de exemplo ao banco de dados
"""
from app import create_app
from models import db, Project
from datetime import datetime

def add_sample_projects():
    app = create_app()
    
    with app.app_context():
        # Verificar se já existem projetos
        existing = Project.query.count()
        print(f"Projetos existentes: {existing}")
        
        if existing > 0:
            print("Já existem projetos no banco de dados!")
            return
        
        # Criar projetos de exemplo
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
            }
        ]
        
        for proj_data in projects:
            project = Project(**proj_data)
            db.session.add(project)
        
        db.session.commit()
        print(f"✓ {len(projects)} projetos adicionados com sucesso!")
        
        # Listar projetos
        all_projects = Project.query.all()
        print("\nProjetos no banco:")
        for p in all_projects:
            print(f"  - {p.title}")

if __name__ == '__main__':
    add_sample_projects()
