@echo off
echo ====================================
echo   CORRIGINDO BANCO DE DADOS
echo ====================================
echo.

cd /d "%~dp0"

python fix_database.py

echo.
echo Pressione qualquer tecla para fechar...
pause > nul
