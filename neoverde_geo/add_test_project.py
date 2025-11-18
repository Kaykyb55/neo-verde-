from models import db, Project
from app import create_app

app = create_app()

with app.app_context():
    try:
        # Verificar projetos existentes
        existing = Project.query.count()
        print(f"Projetos existentes: {existing}")
        
        # Atualizar projetos existentes com imagens padrão
        projects = Project.query.all()
        for project in projects:
            if not project.image_url or project.image_url == '/static/images/project-default.jpg':
                project.image_url = '/static/uploads/20251025225933_Captura_de_tela_2025-07-03_152730.png'
        
        # Adicionar novo projeto com imagem
        new_project = Project(
            title='Projeto Sustentabilidade Verde',
            description='Projeto de reflorestamento e conservação ambiental em áreas urbanas.',
            category='sustentabilidade',
            image_url='/static/uploads/20251025232506_Captura_de_tela_2025-07-04_180653.png'
        )
            
        db.session.add(new_project)
        db.session.commit()
        
        # Confirmar adição
        new_count = Project.query.count()
        print(f"Projetos após adição: {new_count}")
        print("Projeto adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar projeto: {e}")
        db.session.rollback()