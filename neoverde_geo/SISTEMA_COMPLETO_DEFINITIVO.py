"""
🎯 SISTEMA COMPLETO DEFINITIVO - Refaz TUDO corretamente
Este script deleta tudo e recria TODO o sistema do zero
"""

import os
import sys

# Deleta banco antigo FORÇADAMENTE
print("\n" + "="*80)
print("  🔥 DELETANDO BANCO ANTIGO...")
print("="*80)

db_files = ['database.db', 'instance/database.db', 'neoverde.db']
for db_file in db_files:
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
            print(f"  ✅ Deletado: {db_file}")
        except Exception as e:
            print(f"  ❌ ERRO: {db_file} está sendo usado!")
            print(f"  SOLUÇÃO: Feche o servidor (Ctrl+C) e execute novamente")
            input("\nPressione ENTER para sair...")
            sys.exit(1)

os.makedirs('instance', exist_ok=True)
print("  ✅ Pasta instance criada\n")

# Agora cria tudo do zero
from app import create_app
from models import db, User, Project, Media, ProjectComment
from werkzeug.security import generate_password_hash
from datetime import datetime

print("="*80)
print("  🚀 CRIANDO SISTEMA COMPLETO...")
print("="*80 + "\n")

app = create_app()

with app.app_context():
    # 1. Criar estrutura
    print("[1/5] Criando estrutura do banco...")
    db.create_all()
    print("  ✅ Estrutura criada!\n")
    
    # 2. Criar admin
    print("[2/5] Criando usuário admin...")
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
        print("  ✅ Admin criado!")
    else:
        print("  ✅ Admin já existe!")
    print("  ✅ Email: admin@neoverde.com / Senha: admin123\n")
    
    # 3. Criar 12 projetos
    print("[3/5] Criando 12 projetos...")
    
    projetos = [
        {
            'title': 'Reflorestamento Mata Atlântica',
            'description': 'Recuperação de 500 hectares de Mata Atlântica através do plantio de 50.000 mudas de espécies nativas. Projeto envolve comunidades locais em todas as etapas, desde a produção de mudas até o monitoramento do crescimento. Meta: restaurar corredores ecológicos e aumentar a biodiversidade regional.',
            'category': 'Reflorestamento',
            'image_url': 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=800'
        },
        {
            'title': 'Energia Solar Comunitária',
            'description': 'Instalação de sistemas fotovoltaicos em 200 residências de baixa renda. O projeto reduz custos de energia em até 95% e promove independência energética. Capacitação técnica gratuita para manutenção. Impacto: redução de 300 toneladas de CO2 por ano.',
            'category': 'Energia Renovável',
            'image_url': 'https://images.unsplash.com/photo-1509391366360-2e959784a276?w=800'
        },
        {
            'title': 'Programa Escola Sustentável',
            'description': 'Educação ambiental e reciclagem em 50 escolas públicas. Oficinas de compostagem, hortas escolares orgânicas e coleta seletiva. Mais de 5.000 alunos participam ativamente. Resultados: 80% de redução no desperdício de alimentos.',
            'category': 'Educação Ambiental',
            'image_url': 'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=800'
        },
        {
            'title': 'Proteção de Nascentes',
            'description': 'Recuperação e proteção de 30 nascentes em áreas rurais. Cercamento, reflorestamento ciliar e sistemas de captação sustentável. Beneficia 15 comunidades com água limpa. Monitoramento constante da qualidade da água.',
            'category': 'Recursos Hídricos',
            'image_url': 'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800'
        },
        {
            'title': 'Hortas Urbanas Orgânicas',
            'description': 'Criação de 100 hortas comunitárias em áreas urbanas. Produção orgânica sem agrotóxicos. Segurança alimentar e geração de renda para 300 famílias. Oficinas gratuitas de agricultura urbana. Produção: 2 toneladas de alimentos orgânicos por mês.',
            'category': 'Agricultura Sustentável',
            'image_url': 'https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?w=800'
        },
        {
            'title': 'Limpeza Oceanos e Praias',
            'description': 'Mutirões mensais de limpeza em 20 praias. Remoção de 15 toneladas de resíduos plásticos por ano. Programa de conscientização em escolas. Parceria com pescadores locais. Reciclagem de 90% dos materiais coletados.',
            'category': 'Preservação Marinha',
            'image_url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800'
        },
        {
            'title': 'Telhados Verdes Urbanos',
            'description': 'Implantação de jardins em 50 telhados de edifícios urbanos. Redução de temperatura em até 5°C, economia de energia. Absorção de 200kg de CO2 por telhado/ano. Criação de microhabitats para abelhas e pássaros.',
            'category': 'Urbanismo Verde',
            'image_url': 'https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=800'
        },
        {
            'title': 'Mobilidade Verde',
            'description': 'Implantação de 30km de ciclovias seguras e 20 estações de bike-sharing. Incentivo ao transporte ativo. Oficinas gratuitas de manutenção de bicicletas. Redução estimada: 500 toneladas de CO2/ano.',
            'category': 'Mobilidade Sustentável',
            'image_url': 'https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=800'
        },
        {
            'title': 'Proteção de Polinizadores',
            'description': 'Criação de corredores ecológicos para abelhas. Plantio de 10.000 flores nativas melíferas. Instalação de 100 hotéis de insetos. Educação sobre importância dos polinizadores. Aumento de 40% na população de abelhas nativas.',
            'category': 'Biodiversidade',
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800'
        },
        {
            'title': 'Bosques Nativos Urbanos',
            'description': 'Plantio de mini-bosques com espécies nativas usando método Miyawaki. 10 bosques com 5.000 árvores. Crescimento 10x mais rápido. Redução de ilhas de calor, melhoria da qualidade do ar.',
            'category': 'Reflorestamento Urbano',
            'image_url': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800'
        },
        {
            'title': 'Agricultura Regenerativa',
            'description': 'Transição de 50 propriedades para agricultura regenerativa. Recuperação de solos degradados. Redução de 70% no uso de agrotóxicos. Aumento de 50% na matéria orgânica do solo. Captura de 10 ton de carbono/ha/ano.',
            'category': 'Agricultura Sustentável',
            'image_url': 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=800'
        },
        {
            'title': 'Eficiência Energética',
            'description': 'Programa de eficiência energética em prédios públicos. Substituição por LED, sensores, isolamento térmico. Economia de 40% no consumo. Redução de 200 ton de CO2/ano. Retorno em 2 anos.',
            'category': 'Energia Renovável',
            'image_url': 'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=800'
        }
    ]
    
    for i, proj in enumerate(projetos, 1):
        project = Project(**proj)
        db.session.add(project)
        print(f"  ✅ {i}. {proj['title']}")
    
    db.session.commit()
    print(f"\n  ✅ {len(projetos)} projetos criados!\n")
    
    # 4. Criar 12 fotos
    print("[4/5] Criando 12 fotos na galeria...")
    
    fotos = [
        {'filename': 'floresta.jpg', 'title': 'Floresta Atlântica', 'description': 'Vista aérea de floresta tropical preservada', 'category': 'natureza', 'filetype': 'image/jpeg', 'filesize': 2048000, 'url': 'https://images.unsplash.com/photo-1511497584788-876760111969?w=800'},
        {'filename': 'solar.jpg', 'title': 'Energia Solar', 'description': 'Painéis solares gerando energia limpa', 'category': 'energia-renovavel', 'filetype': 'image/jpeg', 'filesize': 1920000, 'url': 'https://images.unsplash.com/photo-1508514177221-188b1cf16e9d?w=800'},
        {'filename': 'reciclagem.jpg', 'title': 'Reciclagem', 'description': 'Centro de reciclagem comunitário', 'category': 'reciclagem', 'filetype': 'image/jpeg', 'filesize': 1792000, 'url': 'https://images.unsplash.com/photo-1528323273322-d81458248d40?w=800'},
        {'filename': 'nascente.jpg', 'title': 'Nascente Protegida', 'description': 'Água cristalina cercada por vegetação', 'category': 'preservacao', 'filetype': 'image/jpeg', 'filesize': 2304000, 'url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800'},
        {'filename': 'horta.jpg', 'title': 'Horta Comunitária', 'description': 'Produção orgânica de hortaliças', 'category': 'sustentabilidade', 'filetype': 'image/jpeg', 'filesize': 1920000, 'url': 'https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=800'},
        {'filename': 'praia.jpg', 'title': 'Praia Limpa', 'description': 'Praia preservada após mutirão', 'category': 'preservacao', 'filetype': 'image/jpeg', 'filesize': 2560000, 'url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800'},
        {'filename': 'eolica.jpg', 'title': 'Energia Eólica', 'description': 'Turbinas gerando energia limpa', 'category': 'energia-renovavel', 'filetype': 'image/jpeg', 'filesize': 2100000, 'url': 'https://images.unsplash.com/photo-1532601224476-15c79f2f7a51?w=800'},
        {'filename': 'borboleta.jpg', 'title': 'Polinizadores', 'description': 'Borboleta polinizando flores', 'category': 'natureza', 'filetype': 'image/jpeg', 'filesize': 1680000, 'url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800'},
        {'filename': 'educacao.jpg', 'title': 'Educação Ambiental', 'description': 'Crianças aprendendo sustentabilidade', 'category': 'sustentabilidade', 'filetype': 'image/jpeg', 'filesize': 1850000, 'url': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800'},
        {'filename': 'compostagem.jpg', 'title': 'Compostagem', 'description': 'Sistema transformando resíduos em adubo', 'category': 'reciclagem', 'filetype': 'image/jpeg', 'filesize': 1750000, 'url': 'https://images.unsplash.com/photo-1604871000636-074fa5117945?w=800'},
        {'filename': 'ciclovia.jpg', 'title': 'Mobilidade Sustentável', 'description': 'Ciclovia promovendo transporte ativo', 'category': 'sustentabilidade', 'filetype': 'image/jpeg', 'filesize': 1890000, 'url': 'https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=800'},
        {'filename': 'telhado_verde.jpg', 'title': 'Telhado Verde', 'description': 'Jardim em telhado urbano', 'category': 'natureza', 'filetype': 'image/jpeg', 'filesize': 2020000, 'url': 'https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=800'}
    ]
    
    for i, foto in enumerate(fotos, 1):
        media = Media(**foto)
        db.session.add(media)
        print(f"  ✅ {i}. {foto['title']}")
    
    db.session.commit()
    print(f"\n  ✅ {len(fotos)} fotos criadas!\n")
    
    # 5. Verificar
    print("[5/5] Verificando...")
    total_projects = Project.query.count()
    total_media = Media.query.count()
    total_users = User.query.count()
    
    print(f"  ✅ Projetos: {total_projects}")
    print(f"  ✅ Fotos: {total_media}")
    print(f"  ✅ Usuários: {total_users}")
    
    print("\n" + "="*80)
    print("  ✅ SISTEMA COMPLETO CRIADO COM SUCESSO!")
    print("="*80)
    
    print("\n📊 RESUMO:")
    print(f"   • {total_projects} Projetos de Sustentabilidade")
    print(f"   • {total_media} Fotos na Galeria")
    print(f"   • {total_users} Usuários")
    
    print("\n🔐 CREDENCIAIS:")
    print("   Email: admin@neoverde.com")
    print("   Senha: admin123")
    
    print("\n🚀 PRÓXIMOS PASSOS:")
    print("   1. Execute: INICIAR_SERVIDOR.bat")
    print("   2. Acesse: http://localhost:5000")
    print("   3. Faça login e explore!")
    
    print("\n" + "="*80 + "\n")

input("✅ Pressione ENTER para fechar...")
