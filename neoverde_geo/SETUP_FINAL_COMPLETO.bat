@echo off
chcp 65001 > nul
title 🎯 Setup Final Completo - NeoVerde
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                      ║
echo ║          🎯 SETUP FINAL COMPLETO - SISTEMA NEOVERDE                  ║
echo ║                                                                      ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo   Este script vai configurar TUDO para deixar o site 100%% pronto!
echo.
echo   O que será feito:
echo   ✓ Limpar banco de dados antigo
echo   ✓ Criar nova estrutura
echo   ✓ Adicionar 12 projetos completos
echo   ✓ Adicionar 12 fotos profissionais
echo   ✓ Criar usuário admin
echo   ✓ Adicionar comentários de exemplo
echo   ✓ Deixar TUDO funcionando perfeitamente!
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo.
pause
echo.
echo Iniciando configuração...
echo.

cd /d "%~dp0"

"c:\Users\pesso\OneDrive\Desktop\site final de elsonn ja pra entrega\.venv\Scripts\python.exe" SETUP_FINAL_COMPLETO.py

echo.
echo ═══════════════════════════════════════════════════════════════════════
echo.
echo   Próximos passos:
echo   1. Execute: INICIAR_SERVIDOR.bat
echo   2. Acesse: http://localhost:5000
echo   3. Login: admin@neoverde.com / admin123
echo.
echo ═══════════════════════════════════════════════════════════════════════
echo.
pause
