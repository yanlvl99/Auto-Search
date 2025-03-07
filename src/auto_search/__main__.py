import os
import logging
from .web.app import run_server
from .config.settings import LOG_LEVEL, LOG_FILE

def setup_logging():
    """Configura o sistema de logging"""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

def main():
    """Função principal que inicia a aplicação"""
    # Configurar logging
    setup_logging()
    
    # Iniciar servidor web
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    run_server(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main() 