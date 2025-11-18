"""
Rotas de autenticação
"""
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests as google_requests

from models import db, User
from config import Config

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    """Página de login"""
    return render_template('login_modern.html')


@auth_bp.route('/login', methods=['POST'])
def login_post():
    """Processar login"""
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    user = User.query.filter_by(email=email).first()
    
    # Verificar se o usuário existe e a senha está correta
    if not user or not check_password_hash(user.password, password):
        flash('Por favor, verifique seus dados de login e tente novamente.', 'error')
        return redirect(url_for('auth.login'))
    
    # Login bem-sucedido
    session['user_id'] = user.id
    session['user_name'] = user.name
    session['user_email'] = user.email
    session['is_admin'] = user.is_admin
    
    flash(f'Bem-vindo, {user.name}!', 'success')
    
    # Redirecionar para o painel administrativo se for admin
    if user.is_admin:
        return redirect(url_for('main.admin'))
    
    return redirect(url_for('main.index'))


@auth_bp.route('/register', methods=['POST'])
def register_post():
    """Processar cadastro"""
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Verificar se o usuário já existe
    user = User.query.filter_by(email=email).first()
    
    if user:
        flash('Email já cadastrado.', 'error')
        return redirect(url_for('auth.login'))
    
    # Criar novo usuário
    new_user = User(
        name=name,
        email=email,
        password=generate_password_hash(password, method='pbkdf2:sha256')
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
def logout():
    """Fazer logout"""
    session.clear()
    flash('Você saiu com sucesso.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/forgot-password')
def forgot_password():
    """Página de recuperação de senha"""
    flash('Funcionalidade de recuperação de senha em desenvolvimento.', 'info')
    return redirect(url_for('auth.login'))


# OAuth Google Login
@auth_bp.route('/login/google')
def login_google():
    """Iniciar login com Google"""
    try:
        client_secrets = Config.get_google_oauth_config()
        
        flow = Flow.from_client_config(
            client_secrets,
            scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
        )
        flow.redirect_uri = url_for('auth.oauth2callback', _external=True)
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        session['oauth_state'] = state
        return redirect(authorization_url)
    except Exception as e:
        flash(f'Erro ao iniciar login com Google. Verifique as credenciais OAuth.', 'error')
        return redirect(url_for('auth.login'))


@auth_bp.route('/oauth2callback')
def oauth2callback():
    """Callback do OAuth Google"""
    try:
        state = session.get('oauth_state')
        client_secrets = Config.get_google_oauth_config()
        
        flow = Flow.from_client_config(
            client_secrets,
            scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
            state=state
        )
        flow.redirect_uri = url_for('auth.oauth2callback', _external=True)
        
        # Obter o token de autorização
        authorization_response = request.url
        flow.fetch_token(authorization_response=authorization_response)
        
        # Obter credenciais
        credentials = flow.credentials
        request_session = google_requests.Request()
        
        # Verificar o ID token
        id_info = id_token.verify_oauth2_token(
            credentials.id_token,
            request_session,
            Config.GOOGLE_CLIENT_ID
        )
        
        # Extrair informações do usuário
        google_id = id_info.get('sub')
        email = id_info.get('email')
        name = id_info.get('name', email.split('@')[0])
        
        # Verificar se o usuário já existe
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Criar novo usuário
            user = User(
                name=name,
                email=email,
                password=generate_password_hash(str(uuid.uuid4()), method='pbkdf2:sha256'),
                is_admin=False
            )
            db.session.add(user)
            db.session.commit()
            flash(f'Bem-vindo, {name}! Conta criada com sucesso via Google.', 'success')
        else:
            flash(f'Bem-vindo de volta, {name}!', 'success')
        
        # Fazer login do usuário
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_email'] = user.email
        session['is_admin'] = user.is_admin
        
        # Redirecionar
        if user.is_admin:
            return redirect(url_for('main.admin'))
        return redirect(url_for('main.index'))
        
    except Exception as e:
        flash(f'Erro ao autenticar com Google: {str(e)}', 'error')
        return redirect(url_for('auth.login'))
