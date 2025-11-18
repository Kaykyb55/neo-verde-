@echo off
cd /d "%~dp0"
title NeoVerde - Servidor
color 0A

echo.
echo ============================================================
echo   NEOVERDE GEOGRAFIA - SISTEMA DE GESTAO
echo ============================================================
echo   Ambiente: development
echo   URL: http://localhost:5000
echo ============================================================
echo.
echo   Iniciando servidor...
echo.

"c:\Users\pesso\OneDrive\Desktop\site final de elsonn ja pra entrega\.venv\Scripts\python.exe" app.py

pause
