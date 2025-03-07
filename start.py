#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para iniciar o Auto Search 1.0.2
Este script inicia a aplicação web que permite automatizar pesquisas no Bing.
Compatível com Python 3.8+ (incluindo Python 3.13)
"""

import os
import sys
import logging
import platform
import subprocess
import importlib.util
import re
import webbrowser
import urllib.request
import json

# Verificar versão do Python
python_version = platform.python_version()

# Lista de dependências necessárias
DEPENDENCIES = [
    "flask",
    "flask_socketio",
    "flask_cors",
    "selenium",
    "webdriver_manager",
    "faker"
]

def check_python_update():
    """Verifica se há uma versão mais recente do Python disponível"""
    print("Verificando atualizações do Python...")
    current_version = tuple(map(int, platform.python_version().split('.')))
    
    try:
        # Obtém a versão mais recente do Python da API do Python.org
        with urllib.request.urlopen("https://www.python.org/api/v2/downloads/release/?is_published=true&status=final&version_type=release") as response:
            data = json.loads(response.read().decode())
            
        # Filtra apenas as versões 3.x
        python3_versions = []
        for release in data['results']:
            version = release['name']
            match = re.match(r'Python (\d+)\.(\d+)\.(\d+)', version)
            if match and match.group(1) == '3':
                major, minor, patch = map(int, match.groups())
                python3_versions.append((major, minor, patch))
        
        if not python3_versions:
            print("Não foi possível encontrar informações sobre a versão mais recente do Python.")
            return
            
        latest_version = max(python3_versions)
        latest_version_str = '.'.join(map(str, latest_version))
        
        if latest_version > current_version:
            print(f"Uma nova versão do Python está disponível: {latest_version_str} (você está usando {platform.python_version()})")
            update = input("Deseja abrir a página de download do Python? (S/N): ")
            if update.lower() == 's':
                webbrowser.open("https://www.python.org/downloads/")
                print("Após a instalação, reinicie este aplicativo.")
                sys.exit(0)
        else:
            print(f"Você está usando a versão mais recente do Python ({platform.python_version()}).")
    except Exception as e:
        print(f"Erro ao verificar atualizações do Python: {e}")
        print("Continuando com a versão atual...")

def check_and_install_dependencies():
    """Verifica e instala as dependências necessárias"""
    missing_deps = []
    
    print("Verificando dependências...")
    for dep in DEPENDENCIES:
        if importlib.util.find_spec(dep) is None:
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"Dependências faltando: {', '.join(missing_deps)}")
        
        # No Windows, pergunta se deseja instalar automaticamente
        if platform.system() == "Windows":
            install = input("Deseja instalar as dependências automaticamente? (S/N): ")
            if install.lower() != "s":
                print("Por favor, instale manualmente as dependências necessárias:")
                print(f"pip install {' '.join(missing_deps)}")
                sys.exit(1)
        
        print("Instalando dependências...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_deps)
            print("Dependências instaladas com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao instalar dependências: {e}")
            print("Por favor, instale manualmente as dependências necessárias:")
            print(f"pip install {' '.join(missing_deps)}")
            sys.exit(1)
    else:
        print("Todas as dependências estão instaladas.")

from src.auto_search.web.app import run_server
from src.auto_search.config.settings import LOG_LEVEL, LOG_FILE

def setup_logging():
    """Configura o sistema de logging"""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger("auto_search")
    logger.info(f"Iniciando Auto Search 1.0.2 (Python {python_version})")

def main():
    """Função principal que inicia a aplicação"""
    # Verificar atualizações do Python
    check_python_update()
    
    # Verificar e instalar dependências
    check_and_install_dependencies()
    
    # Configurar logging
    setup_logging()
    
    # Definir configurações do servidor
    host = os.getenv('HOST', '127.0.0.1')  # Usando localhost por padrão para maior segurança
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"\n=== Auto Search 1.0.2 ===")
    print(f"Python: {platform.python_version()}")
    print(f"Modo: threading (compatível com Python 3.13)")
    print(f"Servidor iniciado em http://{host}:{port}")
    print(f"Pressione Ctrl+C para encerrar")
    
    # Iniciar servidor web
    try:
        run_server(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário.")
    except Exception as e:
        print(f"\nErro ao iniciar o servidor: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 