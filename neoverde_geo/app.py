"""
NeoVerde Geografia - Aplicação Web
Versão Refatorada e Organizada

Este é o arquivo principal da aplicação Flask.
Configurações, modelos e rotas estão separados em módulos.
"""
import os
from dotenv import load_dotenv
from flask import Flask
from werkzeug.security import generate_password_hash

from config import config
from models import db, User

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


def create_app(config_name='development'):
    """
    Factory function para criar a aplicação Flask
    
    Args:
        config_name (str): Nome da configuração ('development', 'production', 'testing')
    
    Returns:
        Flask: Instância da aplicação Flask
    """
    app = Flask(__name__)
    
    # Carrega configurações
    app.config.from_object(config[config_name])
    
    # Configura variável de ambiente OAuth
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = app.config['OAUTHLIB_INSECURE_TRANSPORT']
    
    # Inicializa extensões
    db.init_app(app)
    
    # Registra blueprints (rotas)
    from routes import init_routes
    init_routes(app)
    
    # Cria diretório de uploads se não existir
    upload_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    os.makedirs(upload_path, exist_ok=True)
    
    # Inicializa banco de dados e cria usuário admin
    with app.app_context():
        db.create_all()
        create_admin_user()
    
    return app


def create_admin_user():
    """Cria usuário administrador padrão se não existir"""
    admin_email = 'admin@neoverde.com'
    admin = User.query.filter_by(email=admin_email).first()
    
    if not admin:
        admin_user = User(
            name='Administrador',
            email=admin_email,
            password=generate_password_hash('admin123', method='pbkdf2:sha256'),
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print('✓ Usuário administrador criado!')
        print(f'  Email: {admin_email}')
        print('  Senha: admin123')
        print('  IMPORTANTE: Altere a senha após o primeiro login!')
    else:
        # Garante que o usuário tenha privilégios de administrador
        if not admin.is_admin:
            admin.is_admin = True
            db.session.commit()
            print('✓ Privilégios de administrador atualizados!')
        else:
            print('✓ Usuário administrador já existe!')


if __name__ == '__main__':
    # Determina o ambiente (development, production, testing)
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Cria a aplicação
    app = create_app(env)
    
    # Executa o servidor
    print('\n' + '='*60)
    print('  NeoVerde Geografia - Sistema de Gestão')
    print('='*60)
    print(f'  Ambiente: {env}')
    print(f'  URL: http://localhost:5000')
    print('='*60 + '\n')
    
    app.run(debug=True, host='0.0.0.0', port=5000)