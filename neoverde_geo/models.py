"""
Modelos de dados do aplicativo NeoVerde Geografia
"""
import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Modelo de usuários do sistema"""
    __tablename__ = 'user'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.email}>'


class Media(db.Model):
    """Modelo de mídia (galeria de imagens e vídeos)"""
    __tablename__ = 'media'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = db.Column(db.String(255), nullable=False)
    filetype = db.Column(db.String(50), nullable=False)
    filesize = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    title = db.Column(db.String(200))
    url = db.Column(db.String(500))
    likes_count = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    
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
            'title': self.title or self.filename,
            'url': self.url,
            'likes_count': len(self.likes),
            'comments_count': len(self.comments),
            'views': self.views or 0
        }


class Project(db.Model):
    """Modelo de projetos"""
    __tablename__ = 'project'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))       # URL da imagem
    category = db.Column(db.String(100))
    likes_count = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    comments = db.relationship('ProjectComment', backref='project', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('ProjectLike', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'category': self.category,
            'likes_count': len(self.likes),
            'comments_count': len(self.comments),
            'views': self.views or 0,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Comment(db.Model):
    """Modelo de comentários"""
    __tablename__ = 'comment'
    
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


class Like(db.Model):
    """Modelo de curtidas"""
    __tablename__ = 'like'
    
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


class ProjectComment(db.Model):
    """Modelo de comentários para projetos"""
    __tablename__ = 'project_comment'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('project.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100))
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_name': self.user_name,
            'text': self.text,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class ProjectLike(db.Model):
    """Modelo de curtidas para projetos"""
    __tablename__ = 'project_like'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('project.id'), nullable=False)
    user_identifier = db.Column(db.String(100), nullable=False)  # IP ou session ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class ContactMessage(db.Model):
    """Modelo de mensagens de contato"""
    __tablename__ = 'contact_message'
    
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
