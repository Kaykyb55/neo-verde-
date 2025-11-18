


import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import json
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests as google_requests
import pathlib

# Configuração do aplicativo Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'neoverde-secret-key') # ATENÇÃO: Em produção, mude 'neoverde-secret-key' para uma string aleatória e complexa!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB limite de upload

# Configuração OAuth Google
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Apenas para desenvolvimento
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'SEU_GOOGLE_CLIENT_ID_AQUI')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', 'SEU_GOOGLE_CLIENT_SECRET_AQUI')

# Configuração do Flow OAuth
client_secrets = {
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost:5000/oauth2callback"]
    }
}

# Extensões permitidas
ALLOWED_EXTENSIONS = {
    'image': {'png', 'jpg', 'jpeg', 'gif', 'svg'},
    'video': {'mp4', 'avi', 'mov'}
}

# Inicialização do banco de dados
db = SQLAlchemy(app)

# Modelo de dados para usuários
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.email}>'

# Modelo de dados para mídia (Galeria)
class Media(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = db.Column(db.String(255), nullable=False)
    filetype = db.Column(db.String(50), nullable=False)
    filesize = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    url = db.Column(db.String(500))
    likes_count = db.Column(db.Integer, default=0)
    
    # Relacionamentos
    comments = db.relationship('Comment', backref='media', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='media', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'filetype': self.filetype,
            'filesize': self.filesize,
            'upload_date': self.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
            'category': self.category,
            'description': self.description,
            'url': self.url,
            'likes_count': self.likes_count,
            'comments_count': len(self.comments)
        }

# Modelo de dados para Projetos
class Project(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'category': self.category,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Modelo de dados para Comentários
class Comment(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    media_id = db.Column(db.String(36), db.ForeignKey('media.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100))
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'media_id': self.media_id,
            'user_name': self.user_name,
            'text': self.text,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Modelo de dados para Curtidas
class Like(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    media_id = db.Column(db.String(36), db.ForeignKey('media.id'), nullable=False)
    user_identifier = db.Column(db.String(100), nullable=False)  # IP ou session ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'media_id': self.media_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Modelo de dados para Mensagens de Contato
class ContactMessage(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='unread')  # 'unread', 'read', 'replied'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Funções auxiliares
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in \
           {ext for exts in ALLOWED_EXTENSIONS.values() for ext in exts}

def get_file_type(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    for file_type, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return f"{file_type}/{ext}"
    return "application/octet-stream"

# Rotas do site
@app.route('/')
def index():
    return render_template('index_new.html')

@app.route('/admin')
def admin():
    # Verificação de autenticação para o admin
    if not session.get('user_id'):
        flash('Você precisa estar logado para acessar o painel administrativo.', 'error')
        return redirect(url_for('login'))
    
    # Verificar se o usuário é administrador
    user = User.query.filter_by(id=session.get('user_id')).first()
    if not user or not user.is_admin:
        flash('Você não tem permissão para acessar o painel administrativo.', 'error')
        return redirect(url_for('index'))
    
    return render_template('admin_new.html')

@app.route('/login')
def login():
    return render_template('login_modern.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    user = User.query.filter_by(email=email).first()
    
    # Verificar se o usuário existe e a senha está correta
    if not user or not check_password_hash(user.password, password):
        flash('Por favor, verifique seus dados de login e tente novamente.', 'error')
        return redirect(url_for('login'))
    
    # Se chegou aqui, o usuário existe e a senha está correta
    session['user_id'] = user.id
    session['user_name'] = user.name
    session['user_email'] = user.email
    session['is_admin'] = user.is_admin
    
    flash(f'Bem-vindo, {user.name}!', 'success')
    
    # Redirecionar para o painel administrativo se for admin
    if user.is_admin:
        return redirect(url_for('admin'))
    
    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Verificar se o usuário já existe
    user = User.query.filter_by(email=email).first()
    
    if user:
        flash('Email já cadastrado.')
        return redirect(url_for('login'))
    
    # Criar novo usuário
    new_user = User(
        name=name,
        email=email,
        password=generate_password_hash(password, method='pbkdf2:sha256')
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    flash('Cadastro realizado com sucesso! Faça login para continuar.')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_email', None)
    return redirect(url_for('index'))

@app.route('/forgot-password')
def forgot_password():
    # Esta rota seria para implementar a recuperação de senha
    # Por simplicidade, apenas redirecionamos para a página de login
    flash('Funcionalidade de recuperação de senha em desenvolvimento.')
    return redirect(url_for('login'))

# OAuth Google Login
@app.route('/login/google')
def login_google():
    try:
        flow = Flow.from_client_config(
            client_secrets,
            scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
        )
        flow.redirect_uri = url_for('oauth2callback', _external=True)
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        session['oauth_state'] = state
        return redirect(authorization_url)
    except Exception as e:
        flash(f'Erro ao iniciar login com Google. Verifique as credenciais OAuth.', 'error')
        return redirect(url_for('login'))

@app.route('/oauth2callback')
def oauth2callback():
    try:
        state = session.get('oauth_state')
        
        flow = Flow.from_client_config(
            client_secrets,
            scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
            state=state
        )
        flow.redirect_uri = url_for('oauth2callback', _external=True)
        
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
            GOOGLE_CLIENT_ID
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
                password=generate_password_hash(str(uuid.uuid4()), method='pbkdf2:sha256'),  # Senha aleatória
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
        
        # Redirecionar para admin se for admin, senão para index
        if user.is_admin:
            return redirect(url_for('admin'))
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'Erro ao autenticar com Google: {str(e)}', 'error')
        return redirect(url_for('login'))

# API endpoints
@app.route('/api/media')
def get_media():
    category = request.args.get('category')
    query = Media.query
    
    if category:
        query = query.filter_by(category=category)
    
    media_list = query.order_by(Media.upload_date.desc()).all()
    return jsonify([media.to_dict() for media in media_list])

@app.route('/api/media/upload', methods=['POST'])
def upload_media():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    category = request.form.get('category', 'sustentabilidade')
    description = request.form.get('description', '')
    
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    if file and allowed_file(file.filename):
        # Sanitiza o nome do arquivo e adiciona timestamp
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{filename}"
        
        # Salva o arquivo
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        full_path = os.path.join(app.root_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        file.save(full_path)
        
        # Cria registro no banco de dados
        file_size = os.path.getsize(full_path)
        file_type = get_file_type(filename)
        url = url_for('static', filename=f'uploads/{filename}')
        
        new_media = Media(
            filename=filename,
            filetype=file_type,
            filesize=file_size,
            category=category,
            description=description,
            url=url
        )
        
        db.session.add(new_media)
        db.session.commit()
        
        return jsonify(new_media.to_dict()), 201
    
    return jsonify({'error': 'Tipo de arquivo não permitido'}), 400

@app.route('/api/media/<id>', methods=['DELETE'])
def delete_media(id):
    media = Media.query.get_or_404(id)
    
    # Remove o arquivo físico
    file_path = os.path.join(app.root_path, 'static', 'uploads', media.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Remove o registro do banco de dados
    db.session.delete(media)
    db.session.commit()
    
    return jsonify({'message': 'Mídia excluída com sucesso'}), 200

# API para Projetos
@app.route('/api/projects')
def get_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return jsonify([project.to_dict() for project in projects])

@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    new_project = Project(
        title=data.get('title'),
        description=data.get('description'),
        image_url=data.get('image_url'),
        category=data.get('category', 'geral')
    )
    db.session.add(new_project)
    db.session.commit()
    return jsonify(new_project.to_dict()), 201

@app.route('/api/projects/<id>', methods=['PUT'])
def update_project(id):
    project = Project.query.get_or_404(id)
    data = request.get_json()
    
    project.title = data.get('title', project.title)
    project.description = data.get('description', project.description)
    project.image_url = data.get('image_url', project.image_url)
    project.category = data.get('category', project.category)
    
    db.session.commit()
    return jsonify(project.to_dict())

@app.route('/api/projects/<id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Projeto excluído com sucesso'}), 200

# API para Comentários
@app.route('/api/media/<media_id>/comments')
def get_comments(media_id):
    comments = Comment.query.filter_by(media_id=media_id).order_by(Comment.created_at.desc()).all()
    return jsonify([comment.to_dict() for comment in comments])

@app.route('/api/media/<media_id>/comments', methods=['POST'])
def add_comment(media_id):
    data = request.get_json()
    new_comment = Comment(
        media_id=media_id,
        user_name=data.get('user_name'),
        user_email=data.get('user_email'),
        text=data.get('text')
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify(new_comment.to_dict()), 201

@app.route('/api/comments/<id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comentário excluído com sucesso'}), 200

# API para Curtidas
@app.route('/api/media/<media_id>/like', methods=['POST'])
def toggle_like(media_id):
    user_identifier = request.remote_addr  # Usa IP como identificador
    
    # Verifica se já curtiu
    existing_like = Like.query.filter_by(media_id=media_id, user_identifier=user_identifier).first()
    
    if existing_like:
        # Remove curtida
        db.session.delete(existing_like)
        media = Media.query.get(media_id)
        media.likes_count = max(0, media.likes_count - 1)
        db.session.commit()
        return jsonify({'liked': False, 'likes_count': media.likes_count})
    else:
        # Adiciona curtida
        new_like = Like(media_id=media_id, user_identifier=user_identifier)
        db.session.add(new_like)
        media = Media.query.get(media_id)
        media.likes_count += 1
        db.session.commit()
        return jsonify({'liked': True, 'likes_count': media.likes_count})

@app.route('/api/media/<media_id>/liked')
def check_liked(media_id):
    user_identifier = request.remote_addr
    liked = Like.query.filter_by(media_id=media_id, user_identifier=user_identifier).first() is not None
    return jsonify({'liked': liked})

# API para Mensagens de Contato
@app.route('/api/contact', methods=['POST'])
def send_contact_message():
    data = request.get_json()
    new_message = ContactMessage(
        email=data.get('email'),
        message=data.get('message')
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

@app.route('/api/contact/messages')
def get_contact_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return jsonify([message.to_dict() for message in messages])

@app.route('/api/contact/messages/<id>/status', methods=['PUT'])
def update_message_status(id):
    message = ContactMessage.query.get_or_404(id)
    data = request.get_json()
    message.status = data.get('status', message.status)
    db.session.commit()
    return jsonify(message.to_dict())

@app.route('/api/contact/messages/<id>', methods=['DELETE'])
def delete_message(id):
    message = ContactMessage.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Mensagem excluída com sucesso'}), 200

# API para estatísticas de usuários
@app.route('/api/stats/users')
def get_users_stats():
    total_users = User.query.count()
    admin_users = User.query.filter_by(is_admin=True).count()
    return jsonify({
        'total': total_users,
        'admins': admin_users,
        'regular': total_users - admin_users
    })

# Inicialização do banco de dados
# O decorador before_first_request foi removido nas versões recentes do Flask
# A inicialização do banco de dados é feita no bloco if __name__ == '__main__'

# Função para criar usuário administrador padrão
def create_admin_user():
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
        print('Usuário administrador criado com sucesso!')
    else:
        # Atualiza o usuário existente para ter privilégios de administrador
        if not admin.is_admin:
            admin.is_admin = True
            db.session.commit()
            print('Usuário administrador atualizado com privilégios de administrador!')
        else:
            print('Usuário administrador já existe!')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_user()
    app.run(debug=True)