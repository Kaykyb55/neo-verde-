from models import db, Project
from app import create_app

app = create_app()

with app.app_context():
    try:
        # Verificar projetos existentes
        projects = Project.query.all()
        print(f"Total de projetos: {len(projects)}")
        
        # Mostrar detalhes de cada projeto
        for p in projects:
            print(f"ID: {p.id}, Título: {p.title}, Imagem: {p.image_url}")
            
        # Atualizar todos os projetos com imagens reais
        for project in projects:
            if not project.image_url or project.image_url == '/static/images/project-default.jpg':
                project.image_url = '/static/uploads/20251025225933_Captura_de_tela_2025-07-03_152730.png'
                print(f"Atualizando imagem do projeto {project.id}: {project.title}")
        
        db.session.commit()
        print("Projetos atualizados com sucesso!")
        
    except Exception as e:
        print(f"Erro: {e}")
        db.session.rollback()