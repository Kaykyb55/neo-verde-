"""
🔥 FORÇAR REFAZER - Deleta TUDO e recria do zero (mesmo se houver erros)
"""
import os
import sys
import time

def deletar_todos_bancos():
    """Deleta todos os arquivos de banco de dados"""
    print("\n🔥 DELETANDO TODOS OS BANCOS DE DADOS...")
    
    arquivos_para_deletar = [
        'database.db',
        'instance/database.db',
        'neoverde.db',
        'instance/neoverde.db'
    ]
    
    deletados = 0
    for arquivo in arquivos_para_deletar:
        if os.path.exists(arquivo):
            try:
                os.remove(arquivo)
                print(f"   ✅ Deletado: {arquivo}")
                deletados += 1
            except PermissionError:
                print(f"   ⚠️  {arquivo} está sendo usado. Tentando forçar...")
                time.sleep(1)
                try:
                    os.remove(arquivo)
                    print(f"   ✅ Deletado: {arquivo}")
                    deletados += 1
                except:
                    print(f"   ❌ Não foi possível deletar {arquivo}")
                    print(f"      FECHE O SERVIDOR e execute novamente!")
            except Exception as e:
                print(f"   ❌ Erro ao deletar {arquivo}: {str(e)}")
    
    if deletados == 0:
        print("   ℹ️  Nenhum banco encontrado (começando limpo!)")
    else:
        print(f"\n   ✅ {deletados} arquivo(s) deletado(s)!")
    
    # Criar pasta instance
    os.makedirs('instance', exist_ok=True)
    print("   ✅ Pasta instance criada/verificada")
    
    return True

if __name__ == '__main__':
    print("="*80)
    print("  🔥 FORÇAR DELEÇÃO DO BANCO DE DADOS")
    print("="*80)
    print("\n  AVISO: Isso vai DELETAR o banco de dados atual!")
    print("  Certifique-se de que o SERVIDOR ESTÁ PARADO (Ctrl+C)\n")
    
    input("Pressione ENTER para continuar...")
    
    if deletar_todos_bancos():
        print("\n" + "="*80)
        print("  ✅ BANCO DELETADO COM SUCESSO!")
        print("="*80)
        print("\n  AGORA execute:")
        print("     py REFAZER_TUDO_DO_ZERO.py")
        print("\n" + "="*80)
    else:
        print("\n" + "="*80)
        print("  ❌ ERRO AO DELETAR BANCO")
        print("="*80)
        print("\n  SOLUÇÃO:")
        print("  1. PARE o servidor (Ctrl+C no terminal)")
        print("  2. Execute este script novamente")
        print("\n" + "="*80)
    
    input("\nPressione ENTER para fechar...")
