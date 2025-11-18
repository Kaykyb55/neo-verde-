@echo off
chcp 65001 > nul
title 🚀 Arrumando TUDO - Sistema NeoVerde

echo.
echo ═══════════════════════════════════════════════════════════
echo   🚀 ARRUMANDO TUDO - SISTEMA NEOVERDE
echo ═══════════════════════════════════════════════════════════
echo.
echo   Este script vai configurar TUDO automaticamente:
echo   ✓ Banco de dados
echo   ✓ Usuário administrador  
echo   ✓ Projetos de exemplo
echo   ✓ Galeria de fotos
echo   ✓ Todas as funcionalidades
echo.
echo ═══════════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

py ARRUMAR_TUDO.py

if errorlevel 1 (
    echo.
    echo ❌ Erro ao executar o script!
    echo.
    echo Tentando com python...
    python ARRUMAR_TUDO.py
)

if errorlevel 1 (
    echo.
    echo ❌ Erro ao executar o script!
    echo.
    echo Tentando com python3...
    python3 ARRUMAR_TUDO.py
)

echo.
pause
