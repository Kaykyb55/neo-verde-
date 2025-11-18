@echo off
chcp 65001 > nul
title 🔥 Solução Completa - NeoVerde

color 0E
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                      ║
echo ║        🔥 SOLUÇÃO COMPLETA - DELETA E RECRIA TUDO 🔥                 ║
echo ║                                                                      ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo   ⚠️  IMPORTANTE: PARE O SERVIDOR ANTES!
echo.
echo   Se o servidor estiver rodando:
echo   1. Vá no terminal onde ele está rodando
echo   2. Pressione Ctrl+C para parar
echo   3. Volte aqui e continue
echo.
pause
echo.

cd /d "%~dp0"

echo ═══════════════════════════════════════════════════════════════════════
echo   PASSO 1: Deletando banco antigo...
echo ═══════════════════════════════════════════════════════════════════════
echo.

py FORCAR_REFAZER.py

echo.
echo ═══════════════════════════════════════════════════════════════════════
echo   PASSO 2: Recriando tudo do zero...
echo ═══════════════════════════════════════════════════════════════════════
echo.

timeout /t 2 > nul

py REFAZER_TUDO_DO_ZERO.py

echo.
echo ═══════════════════════════════════════════════════════════════════════
echo   ✅ CONCLUÍDO!
echo ═══════════════════════════════════════════════════════════════════════
echo.
echo   AGORA:
echo   1. Inicie o servidor: py app.py
echo   2. Acesse: http://localhost:5000
echo   3. Login: admin@neoverde.com / admin123
echo.
pause
