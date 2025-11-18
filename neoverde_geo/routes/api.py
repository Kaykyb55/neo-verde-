"""
Rotas da API REST
"""
import os
from datetime import datetime
from flask import Blueprint, request, jsonify, url_for, current_app, session
from werkzeug.utils import secure_filename

from models import db, Media, Project, Comment, Like, ContactMessage, User, ProjectComment, ProjectLike
from config import Config

api_bp = Blueprint('api', __name__)

def check_api_auth():
    """Verifica autenticação para API e retorna JSON em vez de redirecionar"""
    if not session.get('user_id'):
        return False
    return True


def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in \
           {ext for exts in Config.ALLOWED_EXTENSIONS.values() for ext in exts}


def get_file_type(filename):
    """Retorna o tipo MIME do arquivo"""
    ext = filename.rsplit('.', 1)[1].lower()
    for file_type, extensions in Config.ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return f"{file_type}/{ext}"
    return "application/octet-stream"


# ======================
# ROTAS DE MÍDIA
# ======================

@api_bp.route('/media')
def get_media():
    """Listar mídia (galeria)"""
    # Verificação de autenticação para API pública
    category = request.args.get('category')
    query = Media.query
    
    if category:
        query = query.filter_by(category=category)
    
    media_list = query.order_by(Media.upload_date.desc()).all()
    return jsonify([media.to_dict() for media in media_list])


@api_bp.route('/media/upload', methods=['POST'])
def upload_media():
    """Upload de arquivo de mídia"""
    # Verificação de autenticação para API administrativa
    if not check_api_auth():
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        category = request.form.get('category', 'sustentabilidade')
        description = request.form.get('description', '')
        title = request.form.get('title', '')
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if file and allowed_file(file.filename):
            # Sanitiza o nome do arquivo e adiciona timestamp
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            # Cria o caminho completo para o diretório de uploads
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Salva o arquivo
            full_path = os.path.join(upload_dir, filename)
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
                title=title or filename,
                url=url
            )
            
            db.session.add(new_media)
            db.session.commit()
            
            return jsonify(new_media.to_dict()), 201
        
        return jsonify({'error': 'Tipo de arquivo não permitido'}), 400
    
    except Exception as e:
        print(f"Erro ao fazer upload: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Erro ao processar upload: {str(e)}'}), 500


@api_bp.route('/media/<id>', methods=['PUT'])
def update_media(id):
    """Atualizar mídia (apenas metadados)"""
    if not check_api_auth():
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    try:
        media = Media.query.get_or_404(id)
        data = request.get_json()
        
        # Atualizar campos
        if data.get('title'):
            media.title = data.get('title')
        if data.get('description'):
            media.description = data.get('description')
        if data.get('category'):
            media.category = data.get('category')
        
        db.session.commit()
        return jsonify(media.to_dict()), 200
    
    except Exception as e:
        print(f"Erro ao atualizar mídia: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Erro ao atualizar mídia: {str(e)}'}), 500


@api_bp.route('/media/<id>', methods=['DELETE'])
def delete_media(id):
    """Deletar mídia"""
    media = Media.query.get_or_404(id)
    
    # Remove o arquivo físico
    file_path = os.path.join(current_app.root_path, 'static', 'uploads', media.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Remove o registro do banco de dados
    db.session.delete(media)
    db.session.commit()
    
    return jsonify({'message': 'Mídia excluída com sucesso'}), 200


# ======================
# ROTAS DE PROJETOS
# ======================

@api_bp.route('/projects')
def get_projects():
    """Listar projetos"""
    try:
        # Rota pública - sem verificação de autenticação
        projects = Project.query.order_by(Project.created_at.desc()).all()
        return jsonify([project.to_dict() for project in projects])
    except Exception as e:
        print(f"Erro ao buscar projetos: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'projects': []}), 500


@api_bp.route('/projects', methods=['POST'])
def create_project():
    """Criar projeto"""
    # Verificação de autenticação para API administrativa
    if not check_api_auth():
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    try:
        # Verifica se é um envio de formulário com arquivo ou JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Processamento de formulário com upload de arquivo
            title = request.form.get('title')
            description = request.form.get('description')
            category = request.form.get('category', 'geral')
            
            if not title or not description:
                return jsonify({'error': 'Título e descrição são obrigatórios'}), 400
            
            # Verifica se há arquivo enviado
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '' and allowed_file(file.filename):
                    # Sanitiza o nome do arquivo e adiciona timestamp
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    filename = f"project_{timestamp}_{filename}"
                    
                    # Cria o caminho completo para o diretório de uploads
                    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    # Salva o arquivo
                    full_path = os.path.join(upload_dir, filename)
                    file.save(full_path)
                    
                    # URL para acesso ao arquivo
                    image_url = url_for('static', filename=f'uploads/{filename}')
                    
                    # Cria o projeto com o arquivo local
                    new_project = Project(
                        title=title,
                        description=description,
                        image_url=image_url,
                        category=category
                    )
                    
                    db.session.add(new_project)
                    db.session.commit()
                    return jsonify(new_project.to_dict()), 201
                else:
                    return jsonify({'error': 'Arquivo inválido ou tipo não permitido'}), 400
            
            return jsonify({'error': 'Nenhuma imagem enviada'}), 400
        else:
            # Processamento tradicional via JSON (mantido para compatibilidade)
            data = request.get_json()
            
            if not data or not data.get('title') or not data.get('description'):
                return jsonify({'error': 'Título e descrição são obrigatórios'}), 400
            
            new_project = Project(
                title=data.get('title'),
                description=data.get('description'),
                image_url=data.get('image_url'),
                category=data.get('category', 'geral')
            )
            db.session.add(new_project)
            db.session.commit()
            return jsonify(new_project.to_dict()), 201
    
    except Exception as e:
        print(f"Erro ao criar projeto: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Erro ao processar projeto: {str(e)}'}), 500


@api_bp.route('/projects/<id>', methods=['PUT'])
def update_project(id):
    """Atualizar projeto"""
    if not check_api_auth():
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    try:
        project = Project.query.get_or_404(id)
        
        # Verifica se é upload de arquivo ou JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Atualização com upload de novo arquivo
            title = request.form.get('title')
            description = request.form.get('description')
            category = request.form.get('category')
            
            if title:
                project.title = title
            if description:
                project.description = description
            if category:
                project.category = category
            
            # Se há novo arquivo de imagem
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '' and allowed_file(file.filename):
                    # Sanitiza o nome do arquivo e adiciona timestamp
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    filename = f"project_{timestamp}_{filename}"
                    
                    # Cria o caminho completo para o diretório de uploads
                    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    # Salva o arquivo
                    full_path = os.path.join(upload_dir, filename)
                    file.save(full_path)
                    
                    # Atualiza URL da imagem
                    project.image_url = url_for('static', filename=f'uploads/{filename}')
        else:
            # Atualização via JSON
            data = request.get_json()
            
            if data.get('title'):
                project.title = data.get('title')
            if data.get('description'):
                project.description = data.get('description')
            if data.get('image_url'):
                project.image_url = data.get('image_url')
            if data.get('category'):
                project.category = data.get('category')
        
        db.session.commit()
        return jsonify(project.to_dict()), 200
    
    except Exception as e:
        print(f"Erro ao atualizar projeto: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Erro ao atualizar projeto: {str(e)}'}), 500


@api_bp.route('/projects/<id>', methods=['DELETE'])
def delete_project(id):
    """Deletar projeto"""
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Projeto excluído com sucesso'}), 200


# ======================
# ROTAS DE COMENTÁRIOS
# ======================

@api_bp.route('/media/<media_id>/comments')
def get_comments(media_id):
    """Listar comentários de uma mídia"""
    comments = Comment.query.filter_by(media_id=media_id).order_by(Comment.created_at.desc()).all()
    return jsonify([comment.to_dict() for comment in comments])


@api_bp.route('/media/<media_id>/comments', methods=['POST'])
def add_comment(media_id):
    """Adicionar comentário"""
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


@api_bp.route('/comments/<id>', methods=['DELETE'])
def delete_comment(id):
    """Deletar comentário"""
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comentário excluído com sucesso'}), 200


# ======================
# ROTAS DE CURTIDAS
# ======================

@api_bp.route('/media/<media_id>/like', methods=['POST'])
def toggle_like(media_id):
    """Curtir/descurtir mídia"""
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


@api_bp.route('/media/<media_id>/liked')
def check_liked(media_id):
    """Verificar se mídia foi curtida"""
    user_identifier = request.remote_addr
    liked = Like.query.filter_by(media_id=media_id, user_identifier=user_identifier).first() is not None
    return jsonify({'liked': liked})


# ======================
# ROTAS DE CONTATO
# ======================

@api_bp.route('/contact', methods=['POST'])
def submit_contact():
    """Enviar mensagem de contato"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('message'):
        return jsonify({'success': False, 'error': 'Email e mensagem são obrigatórios'}), 400
    
    new_message = ContactMessage(
        email=data.get('email'),
        message=data.get('message')
    )
    
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Mensagem enviada com sucesso!'}), 201


@api_bp.route('/projects/<project_id>/like', methods=['POST'])
def like_project(project_id):
    """Adicionar like a um projeto"""
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Projeto não encontrado'}), 404
    
    user_identifier = request.remote_addr
    
    # Verifica se o usuário já curtiu este projeto
    existing_like = ProjectLike.query.filter_by(
        project_id=project_id,
        user_identifier=user_identifier
    ).first()
    
    if existing_like:
        return jsonify({'error': 'Você já curtiu este projeto'}), 400
    
    # Adiciona o like
    new_like = ProjectLike(
        project_id=project_id,
        user_identifier=user_identifier
    )
    
    # Incrementa o contador de likes
    project.likes_count += 1
    
    db.session.add(new_like)
    db.session.commit()
    
    return jsonify({'success': True, 'likes_count': project.likes_count})


@api_bp.route('/projects/<project_id>/comment', methods=['POST'])
def comment_project(project_id):
    """Adicionar comentário a um projeto"""
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Projeto não encontrado'}), 404
    
    data = request.get_json()
    if not data or not data.get('text') or not data.get('user_name'):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    new_comment = ProjectComment(
        project_id=project_id,
        user_name=data.get('user_name'),
        user_email=data.get('user_email', ''),
        text=data.get('text')
    )
    
    db.session.add(new_comment)
    db.session.commit()
    
    return jsonify({'success': True, 'comment': new_comment.to_dict()})


@api_bp.route('/projects/<project_id>/comments')
def get_project_comments(project_id):
    """Obter comentários de um projeto"""
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Projeto não encontrado'}), 404
    
    comments = ProjectComment.query.filter_by(project_id=project_id).order_by(ProjectComment.created_at.desc()).all()
    return jsonify([comment.to_dict() for comment in comments])


@api_bp.route('/contact/messages')
def get_contact_messages():
    """Listar mensagens de contato"""
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return jsonify([message.to_dict() for message in messages])


@api_bp.route('/contact/messages/<id>/status', methods=['PUT'])
def update_message_status(id):
    """Atualizar status de mensagem"""
    message = ContactMessage.query.get_or_404(id)
    data = request.get_json()
    message.status = data.get('status', message.status)
    db.session.commit()
    return jsonify(message.to_dict())


@api_bp.route('/contact/messages/<id>', methods=['DELETE'])
def delete_message(id):
    """Deletar mensagem"""
    message = ContactMessage.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Mensagem excluída com sucesso'}), 200


# ======================
# ROTAS DE ESTATÍSTICAS
# ======================

@api_bp.route('/stats/users')
def get_users_stats():
    """Estatísticas de usuários"""
    total_users = User.query.count()
    admin_users = User.query.filter_by(is_admin=True).count()
    return jsonify({
        'total': total_users,
        'admins': admin_users,
        'regular': total_users - admin_users
    })
