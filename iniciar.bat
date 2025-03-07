@echo off
title Auto Search - Automação Bing
cls

:: Configurações do ambiente
set PYTHON_PATH=python
set VENV_NAME=.venv
set HOST=localhost
set PORT=5000

:: Verifica se Python está instalado
%PYTHON_PATH% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python não encontrado! Por favor, instale o Python 3.8 ou superior.
    echo Pressione qualquer tecla para abrir a página de download...
    pause >nul
    start https://www.python.org/downloads/
    exit /b 1
)

:: Cria ambiente virtual se não existir
if not exist "%VENV_NAME%" (
    echo Criando ambiente virtual...
    %PYTHON_PATH% -m venv %VENV_NAME%
)

:: Ativa o ambiente virtual
call %VENV_NAME%\Scripts\activate

:: Verifica e instala/atualiza dependências
echo Verificando dependências...
python -m pip install -r requirements.txt

:: Inicia a aplicação
echo Iniciando Auto Search...
echo.
echo Acesse http://%HOST%:%PORT% no seu navegador
echo.
echo Para parar o programa, feche esta janela
echo.
python -m src.auto_search

:: Em caso de erro, mantém a janela aberta
if %errorlevel% neq 0 (
    echo.
    echo Ocorreu um erro! Verifique as mensagens acima.
    pause
) 