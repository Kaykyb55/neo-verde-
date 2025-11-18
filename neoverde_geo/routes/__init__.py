"""
Módulo de rotas do NeoVerde Geografia
"""
from flask import Flask

def init_routes(app: Flask):
    """Inicializa todas as rotas do aplicativo"""
    from .main import main_bp
    from .auth import auth_bp
    from .api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
