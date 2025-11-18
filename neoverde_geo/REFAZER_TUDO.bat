@echo off
chcp 65001 > nul
title 🔄 Refazendo TUDO - Sistema NeoVerde

color 0A
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                      ║
echo ║        🔄 REFAZENDO TODO O SISTEMA NEOVERDE DO ZERO 🔄               ║
echo ║                                                                      ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo   AVISO: Isso vai DELETAR o banco antigo e RECRIAR tudo!
echo.
echo   O que será feito:
echo   ✓ Deletar banco de dados antigo
echo   ✓ Criar estrutura nova
echo   ✓ Adicionar usuário admin
echo   ✓ Adicionar 10 projetos completos
echo   ✓ Adicionar 10 fotos na galeria
echo   ✓ Configurar comentários e curtidas
echo   ✓ Deixar tudo funcionando perfeitamente
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo.
pause
echo.
echo Iniciando...
echo.

cd /d "%~dp0"

py REFAZER_TUDO_DO_ZERO.py

if errorlevel 1 (
    echo.
    echo Tentando com python...
    python REFAZER_TUDO_DO_ZERO.py
)

if errorlevel 1 (
    echo.
    echo Tentando com python3...
    python3 REFAZER_TUDO_DO_ZERO.py
)

echo.
echo ═══════════════════════════════════════════════════════════════════════
echo.
pause
