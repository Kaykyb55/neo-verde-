"""
Executa o script de refazer tudo (sem problemas de caminho)
"""
import subprocess
import sys
import os

# Mudar para o diretório correto
os.chdir(r'c:\Users\pesso\OneDrive\Desktop\site final de elsonn ja pra entrega\neoverde_geo')

# Executar o script
sys.path.insert(0, os.getcwd())

# Importar e executar
exec(open('REFAZER_TUDO_DO_ZERO.py', encoding='utf-8').read())
