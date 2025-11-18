"""
🔄 REFAZER TUDO DO ZERO - Sistema NeoVerde Completo
Este script vai DELETAR o banco antigo e CRIAR TUDO NOVAMENTE
com todas as funcionalidades corretas e completas.
"""

import os
import shutil
from app import create_app
from models import db, User, Project, Media, Comment, Like, ProjectComment, ProjectLike, ContactMessage
from werkzeug.security import generate_password_hash
from datetime import datetime

def print_header(text):
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80)

def print_step(step, text):
    print(f"\n[{step}] {text}")

def print_success(text):
    print(f"   ✅ {text}")

def print_error(text):
    print(f"   ❌ {text}")

def deletar_banco_antigo():
    """Deleta o banco de dados antigo para começar do zero"""
    print_step("1/8", "Limpando banco de dados antigo...")
    
    db_files = ['database.db', 'instance/database.db']
    deleted = False
    
    for db_file in db_files:
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                print_success(f"Deletado: {db_file}")
                deleted = True
            except Exception as e:
                print_error(f"Erro ao deletar {db_file}: {str(e)}")
    
    if not deleted:
        print_success("Nenhum banco antigo encontrado (começando limpo!)")
    
    # Criar pasta instance se não existir
    os.makedirs('instance', exist_ok=True)

def criar_estrutura_banco():
    """Cria toda a estrutura do banco de dados"""
    print_step("2/8", "Criando estrutura completa do banco de dados...")
    
    app = create_app()
    with app.app_context():
        db.create_all()
        print_success("Estrutura do banco criada!")
        print_success("Tabelas: User, Project, Media, Comment, Like, ProjectComment, ProjectLike, ContactMessage")
    
    return app

def criar_usuario_admin(app):
    """Verifica/Cria usuário administrador"""
    print_step("3/8", "Configurando usuário administrador...")
    
    with app.app_context():
        # Verificar se admin já existe (app.py cria automaticamente)
        admin = User.query.filter_by(email='admin@neoverde.com').first()
        
        if not admin:
            admin = User(
                name='Administrador NeoVerde',
                email='admin@neoverde.com',
                password=generate_password_hash('admin123', method='pbkdf2:sha256'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print_success("Admin criado com sucesso!")
        else:
            # Garantir que seja admin
            if not admin.is_admin:
                admin.is_admin = True
                db.session.commit()
            print_success("Admin já existe e está configurado!")
        
        print_success("Email: admin@neoverde.com")
        print_success("Senha: admin123")

def criar_projetos_sustentabilidade(app):
    """Cria projetos de sustentabilidade completos"""
    print_step("4/8", "Criando projetos de sustentabilidade...")
    
    with app.app_context():
        projetos = [
            {
                'title': '🌳 Reflorestamento Mata Atlântica',
                'description': 'Recuperação de 500 hectares de Mata Atlântica degradada através do plantio de 50 mil mudas de espécies nativas. Projeto envolve comunidades locais em todas as etapas, desde a produção de mudas até o monitoramento do crescimento. Meta: restaurar corredores ecológicos e aumentar a biodiversidade regional.',
                'category': 'Reflorestamento',
                'image_url': 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=800&h=500&fit=crop&q=80'
            },
            {
                'title': '☀️ Energia Solar Comunitária',
                'description': 'Instalação de sistemas fotovoltaicos em 200 residências de comunidades de baixa renda. O projeto reduz custos de energia em até 95% e promove independência energética. Capacitação técnica gratuita para manutenção dos sistemas. Impacto: redução de 300 toneladas de CO2 por ano.',
                'category': 'Energia Renovável',
                'image_url': 'https://images.unsplash.com/photo-1509391366360-2e959784a276?w=800&h=500&fit=crop&q=80'
            },
            {
                'title': '♻️ Programa Escola Sustentável',
                'description': 'Educação ambiental e reciclagem em 50 escolas públicas. Oficinas de compostagem, hortas escolares orgânicas e coleta seletiva. Mais de 5 mil alunos participam ativamente. Resultados: 80% de redução no desperdício de alimentos e criação de 50 hortas escolares produtivas.',
                'category': 'Educação Ambiental',
                'image_url': 'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=800&h=500&fit=crop&q=80'
            },
            {
                'title': '💧 Proteção de Nascentes',
                'description': 'Recuperação e proteção de 30 nascentes em áreas rurais. Cercamento, reflorestamento ciliar e sistemas de captação sustentável. Beneficia 15 comunidades com água limpa e abundante. Monitoramento constante da qualidade da água e preservação da fauna aquática.',
                'category': 'Recursos Hídricos',
                'image_url': 'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800&h=500&fit=crop&q=80'
            },
            {
                'title': '🥬 Hortas Urbanas Orgânicas',
                'description': 'Criação de 100 hortas comunitárias em áreas urbanas. Produção orgânica de hortaliças sem agrotóxicos. Segurança alimentar e geração de renda para 300 famílias. Oficinas gratuitas de agricultura urbana e permacultura. Produção média: 2 toneladas de alimentos orgânicos por mês.',
                'category': 'Agricultura Sustentável',
                'image_url': 'https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?w=800&h=500&fit=crop&q=80'
            },
            {
                'title': '🌊 Limpeza Oceanos e Praias',
                'description': 'Mutirões mensais de limpeza em 20 praias e pontos costeiros. Remoção de 15 toneladas de resíduos plásticos por ano. Programa de conscientização sobre poluição marinha em escolas. Parceria com pescadores locais para proteção da vida marinha. Reciclagem de 90% dos materiais coletados.',
                'category': 'Preservação Marinha',
                'image_url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&h=500&fit=crop&q=80'
            },
            {
                'title': '🌿 Telhados Verdes Urbanos',
                'description': 'Implantação de jardins em 50 telhados de edifícios urbanos. Redução de temperatura interna em até 5°C, economia de energia e melhoria da qualidade do ar. Absorção de 200kg de CO2 por telhado/ano. Criação de microhabitats para abelhas e pássaros. Captação de água da chuva integrada.',
                'category': 'Urbanismo Verde',
                'image_url': 'https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=800&h=500&fit=crop&q=80'
            },
            {
                'title': '🚴 Mobilidade Verde',
                'description': 'Implantação de 30km de ciclovias seguras e 20 estações de bike-sharing. Incentivo ao transporte ativo e redução de emissões. Oficinas gratuitas de manutenção de bicicletas. Parceria com empresas para fomentar deslocamento sustentável. Redução estimada: 500 toneladas de CO2/ano.',
                'category': 'Mobilidade Sustentável',
                'image_url': 'https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=800&h=500&fit=crop&q=80'
            },
            {
                'title': '🐝 Proteção de Polinizadores',
                'description': 'Criação de corredores ecológicos para abelhas e outros polinizadores. Plantio de 10 mil flores nativas melíferas em parques e jardins urbanos. Instalação de 100 hotéis de insetos. Educação sobre a importância dos polinizadores. Aumento de 40% na população de abelhas nativas na região.',
                'category': 'Biodiversidade',
                'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=500&fit=crop&q=80'
            },
            {
                'title': '🌲 Bosques Nativos Urbanos',
                'description': 'Plantio de mini-bosques com espécies nativas em áreas urbanas degradadas. Método Miyawaki para crescimento acelerado. 10 bosques criados com 5 mil árvores. Redução de ilhas de calor, melhoria da qualidade do ar e criação de espaços de lazer e convivência comunitária.',
                'category': 'Reflorestamento Urbano',
                'image_url': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&h=500&fit=crop&q=80'
            }
        ]
        
        for i, proj_data in enumerate(projetos, 1):
            projeto = Project(**proj_data)
            db.session.add(projeto)
            print_success(f"{i}. {proj_data['title']}")
        
        db.session.commit()
        print_success(f"Total: {len(projetos)} projetos criados com sucesso!")

def criar_galeria_fotos(app):
    """Cria galeria de fotos"""
    print_step("5/8", "Criando galeria de fotos...")
    
    with app.app_context():
        fotos = [
            {
                'filename': 'floresta_nativa_001.jpg',
                'title': 'Floresta Nativa Preservada',
                'description': 'Vista aérea de floresta tropical brasileira em estado de preservação. Exemplo de biodiversidade rica e ecossistema equilibrado.',
                'category': 'natureza',
                'filetype': 'image/jpeg',
                'filesize': 2048000,
                'url': 'https://images.unsplash.com/photo-1511497584788-876760111969?w=800&h=600&fit=crop&q=80'
            },
            {
                'filename': 'paineis_solares_002.jpg',
                'title': 'Instalação Solar Residencial',
                'description': 'Sistema fotovoltaico instalado em residência, gerando energia limpa e sustentável. Economia de até 95% na conta de luz.',
                'category': 'energia-renovavel',
                'filetype': 'image/jpeg',
                'filesize': 1920000,
                'url': 'https://images.unsplash.com/photo-1508514177221-188b1cf16e9d?w=800&h=600&fit=crop&q=80'
            },
            {
                'filename': 'reciclagem_plastico_003.jpg',
                'title': 'Centro de Reciclagem Comunitário',
                'description': 'Materiais recicláveis separados e prontos para processamento. Gestão adequada de resíduos reduz poluição.',
                'category': 'reciclagem',
                'filetype': 'image/jpeg',
                'filesize': 1792000,
                'url': 'https://images.unsplash.com/photo-1528323273322-d81458248d40?w=800&h=600&fit=crop&q=80'
            },
            {
                'filename': 'nascente_cristalina_004.jpg',
                'title': 'Nascente Protegida',
                'description': 'Nascente de água cristalina cercada por vegetação nativa. Projeto de preservação garante água limpa para comunidades.',
                'category': 'preservacao',
                'filetype': 'image/jpeg',
                'filesize': 2304000,
                'url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&h=600&fit=crop&q=80'
            },
            {
                'filename': 'horta_organica_005.jpg',
                'title': 'Horta Comunitária Produtiva',
                'description': 'Horta urbana com produção orgânica de hortaliças. Segurança alimentar e renda para famílias participantes.',
                'category': 'sustentabilidade',
                'filetype': 'image/jpeg',
                'filesize': 1920000,
                'url': 'https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=800&h=600&fit=crop&q=80'
            },
            {
                'filename': 'praia_limpa_006.jpg',
                'title': 'Praia Preservada',
                'description': 'Praia limpa após mutirão de limpeza. Resultado do trabalho voluntário de centenas de pessoas.',
                'category': 'preservacao',
                'filetype': 'image/jpeg',
                'filesize': 2560000,
                'url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&h=600&fit=crop&q=80'
            },
            {
                'filename': 'energia_eolica_007.jpg',
                'title': 'Parque Eólico Sustentável',
                'description': 'Turbinas eólicas gerando energia limpa e renovável. Fonte importante de energia sustentável.',
                'category': 'energia-renovavel',
                'filetype': 'image/jpeg',
                'filesize': 2100000,
                'url': 'https://images.unsplash.com/photo-1532601224476-15c79f2f7a51?w=800&h=600&fit=crop&q=80'
            },
            {
                'filename': 'biodiversidade_008.jpg',
                'title': 'Biodiversidade em Ação',
                'description': 'Borboleta polinizando flores nativas. A preservação da biodiversidade é essencial para o equilíbrio dos ecossistemas.',
                'category': 'natureza',
                'filetype': 'image/jpeg',
                'filesize': 1680000,
                'url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=600&fit=crop&q=80'
            },
            {
                'filename': 'educacao_ambiental_009.jpg',
                'title': 'Educação Ambiental Infantil',
                'description': 'Crianças aprendendo sobre sustentabilidade e preservação ambiental através de atividades práticas.',
                'category': 'sustentabilidade',
                'filetype': 'image/jpeg',
                'filesize': 1850000,
                'url': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800&h=600&fit=crop&q=80'
            },
            {
                'filename': 'compostagem_010.jpg',
                'title': 'Compostagem Doméstica',
                'description': 'Sistema de compostagem transformando resíduos orgânicos em adubo rico. Redução de lixo e nutrição para plantas.',
                'category': 'reciclagem',
                'filetype': 'image/jpeg',
                'filesize': 1750000,
                'url': 'https://images.unsplash.com/photo-1604871000636-074fa5117945?w=800&h=600&fit=crop&q=80'
            }
        ]
        
        for i, foto_data in enumerate(fotos, 1):
            foto = Media(**foto_data)
            db.session.add(foto)
            print_success(f"{i}. {foto_data['title']}")
        
        db.session.commit()
        print_success(f"Total: {len(fotos)} fotos adicionadas à galeria!")

def criar_usuarios_exemplo(app):
    """Cria alguns usuários de exemplo"""
    print_step("6/8", "Criando usuários de exemplo...")
    
    with app.app_context():
        usuarios = [
            {
                'name': 'João Silva',
                'email': 'joao@exemplo.com',
                'password': generate_password_hash('senha123', method='pbkdf2:sha256'),
                'is_admin': False
            },
            {
                'name': 'Maria Santos',
                'email': 'maria@exemplo.com',
                'password': generate_password_hash('senha123', method='pbkdf2:sha256'),
                'is_admin': False
            },
            {
                'name': 'Pedro Oliveira',
                'email': 'pedro@exemplo.com',
                'password': generate_password_hash('senha123', method='pbkdf2:sha256'),
                'is_admin': False
            }
        ]
        
        for usuario_data in usuarios:
            usuario = User(**usuario_data)
            db.session.add(usuario)
            print_success(f"Usuário: {usuario_data['name']} ({usuario_data['email']})")
        
        db.session.commit()
        print_success(f"Total: {len(usuarios)} usuários de exemplo criados!")

def criar_comentarios_exemplo(app):
    """Cria comentários de exemplo"""
    print_step("7/8", "Adicionando comentários de exemplo...")
    
    with app.app_context():
        # Comentários em projetos
        projetos = Project.query.limit(3).all()
        for projeto in projetos:
            for i in range(2):
                comentario = ProjectComment(
                    project_id=projeto.id,
                    user_name=f"Usuário {i+1}",
                    text=f"Projeto incrível! Estou muito inspirado com essa iniciativa de {projeto.title}. Parabéns!",
                    created_at=datetime.utcnow()
                )
                db.session.add(comentario)
        
        # Comentários em mídia
        midias = Media.query.limit(3).all()
        for midia in midias:
            for i in range(2):
                comentario = Comment(
                    media_id=midia.id,
                    user_name=f"Visitante {i+1}",
                    text=f"Foto maravilhosa! {midia.title} - isso é o que precisamos para um futuro melhor!",
                    created_at=datetime.utcnow()
                )
                db.session.add(comentario)
        
        db.session.commit()
        print_success("Comentários de exemplo adicionados!")

def verificar_e_exibir_resultado(app):
    """Verifica tudo e exibe o resultado final"""
    print_step("8/8", "Verificando sistema...")
    
    with app.app_context():
        total_users = User.query.count()
        total_projects = Project.query.count()
        total_media = Media.query.count()
        total_comments = Comment.query.count() + ProjectComment.query.count()
        
        print_success(f"Usuários: {total_users}")
        print_success(f"Projetos: {total_projects}")
        print_success(f"Fotos na Galeria: {total_media}")
        print_success(f"Comentários: {total_comments}")
        
        print_header("🎉 SISTEMA COMPLETAMENTE REFEI TO E FUNCIONANDO! 🎉")
        
        print("\n📊 ESTATÍSTICAS:")
        print(f"   • {total_users} usuários (1 admin + {total_users-1} comuns)")
        print(f"   • {total_projects} projetos de sustentabilidade")
        print(f"   • {total_media} fotos na galeria")
        print(f"   • {total_comments} comentários")
        
        print("\n🔐 CREDENCIAIS DE ACESSO:")
        print("   Admin:")
        print("   • Email: admin@neoverde.com")
        print("   • Senha: admin123")
        
        print("\n🚀 PRÓXIMOS PASSOS:")
        print("   1. Inicie o servidor: py app.py")
        print("   2. Acesse: http://localhost:5000")
        print("   3. Explore o site completo!")
        print("   4. Faça login como admin para gerenciar")
        
        print("\n✨ FUNCIONALIDADES DISPONÍVEIS:")
        print("   ✅ Dashboard com estatísticas")
        print("   ✅ Projetos clicáveis com modal")
        print("   ✅ Sistema de curtidas em projetos")
        print("   ✅ Comentários em projetos")
        print("   ✅ Galeria de fotos clicável")
        print("   ✅ Sistema de curtidas em fotos")
        print("   ✅ Comentários em fotos")
        print("   ✅ Formulário de contato")
        print("   ✅ Painel administrativo completo")
        print("   ✅ Upload de arquivos")
        print("   ✅ Gerenciamento de projetos")
        print("   ✅ Gerenciamento de galeria")
        print("   ✅ Design moderno e responsivo")
        
        print("\n" + "="*80)
        print("  💚 SISTEMA NEOVERDE - SUSTENTABILIDADE É VIDA 💚")
        print("="*80 + "\n")

def refazer_tudo():
    """Função principal que refaz tudo do zero"""
    print_header("🔄 REFAZENDO TODO O SISTEMA NEOVERDE DO ZERO")
    print("\n  AVISO: Isso vai DELETAR o banco antigo e criar tudo novamente!")
    print("  Todas as funcionalidades serão recriadas corretamente.\n")
    
    try:
        # 1. Deletar banco antigo
        deletar_banco_antigo()
        
        # 2. Criar estrutura
        app = criar_estrutura_banco()
        
        # 3. Criar admin
        criar_usuario_admin(app)
        
        # 4. Criar projetos
        criar_projetos_sustentabilidade(app)
        
        # 5. Criar galeria
        criar_galeria_fotos(app)
        
        # 6. Criar usuários
        criar_usuarios_exemplo(app)
        
        # 7. Criar comentários
        criar_comentarios_exemplo(app)
        
        # 8. Verificar resultado
        verificar_e_exibir_resultado(app)
        
        return True
        
    except Exception as e:
        print_error(f"ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        
        print("\n" + "="*80)
        print("  ❌ ERRO AO REFAZER O SISTEMA")
        print("="*80)
        print("\n💡 Se o servidor estiver rodando:")
        print("   1. Pare o servidor (Ctrl+C)")
        print("   2. Execute este script novamente")
        print("   3. Inicie o servidor novamente\n")
        
        return False

if __name__ == '__main__':
    try:
        sucesso = refazer_tudo()
        if sucesso:
            print("✅ Pressione ENTER para fechar...")
            input()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro fatal: {str(e)}")
        print("\nPressione ENTER para fechar...")
        input()
