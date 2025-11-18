"""
Rotas principais da aplicação
"""
from flask import Blueprint, render_template, redirect, url_for, flash, session
from models import User

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Página inicial"""
    return render_template('index_new.html')


@main_bp.route('/admin')
def admin():
    """Painel administrativo"""
    # Verificação de autenticação
    if not session.get('user_id'):
        flash('Você precisa estar logado para acessar o painel administrativo.', 'error')
        return redirect(url_for('auth.login'))
    
    # Verificar se o usuário é administrador
    user = User.query.filter_by(id=session.get('user_id')).first()
    if not user or not user.is_admin:
        flash('Você não tem permissão para acessar o painel administrativo.', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('admin_new.html')
