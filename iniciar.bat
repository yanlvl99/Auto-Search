@echo off
title Auto Search 1.0.2
color 0A
cls

echo ===================================
echo    Auto Search 1.0.2 - Menu
echo ===================================
echo.

:: Verifica se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Erro: Python não encontrado. Por favor, instale o Python 3.8 ou superior.
    echo Você pode baixar o Python em https://www.python.org/downloads/
    echo.
    echo Pressione qualquer tecla para abrir a página de download do Python...
    pause >nul
    start https://www.python.org/downloads/
    exit /b 1
)

:: Exibe a versão do Python
python --version
echo.

:: Verifica se o ambiente virtual existe
if not exist .venv (
    echo Criando ambiente virtual...
    python -m venv .venv
    echo Ambiente virtual criado com sucesso!
    echo.
)

:: Ativa o ambiente virtual
call .venv\Scripts\activate.bat

:menu
echo Escolha uma opção:
echo.
echo [1] Iniciar Auto Search
echo [2] Verificar atualizações do Python
echo [3] Instalar/Atualizar dependências
echo [4] Sair
echo.
set /p opcao="Digite o número da opção desejada: "

if "%opcao%"=="1" goto iniciar
if "%opcao%"=="2" goto atualizar_python
if "%opcao%"=="3" goto instalar_deps
if "%opcao%"=="4" (
    call deactivate
    goto sair
)

echo.
echo Opção inválida. Por favor, tente novamente.
echo.
goto menu

:iniciar
cls
echo ===================================
echo    Iniciando Auto Search 1.0.2
echo ===================================
echo.

:: Executa o script Python
python start.py

:: Se o script terminar com erro, aguarda antes de fechar
if %errorlevel% neq 0 (
    echo.
    echo O aplicativo foi encerrado com erro.
    pause
)
goto menu

:atualizar_python
cls
echo ===================================
echo    Verificando atualizações do Python
echo ===================================
echo.
start https://www.python.org/downloads/
echo Página de download do Python aberta no navegador.
echo.
echo Após a instalação, reinicie este aplicativo.
echo.
pause
goto menu

:instalar_deps
cls
echo ===================================
echo    Instalando dependências
echo ===================================
echo.
python -m pip install -r requirements.txt
echo.
echo Dependências instaladas/atualizadas.
echo.
pause
goto menu

:sair
exit /b 0 