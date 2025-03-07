import os
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from ..core.automation import EdgeAutomation
from ..core.profiles import detect_edge_profiles
from ..config.settings import (
    SECRET_KEY,
    DEFAULT_SEARCH_COUNT,
    MIN_SEARCH_INTERVAL,
    MAX_SEARCH_INTERVAL
)
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Dicionário para armazenar instâncias ativas de automação
active_automations = {}

@app.route('/')
def index():
    """Renderiza a página principal"""
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """Manipula conexão do WebSocket"""
    profiles = detect_edge_profiles()
    socketio.emit('profiles_updated', profiles)

@socketio.on('refresh_profiles')
def handle_refresh_profiles():
    """Atualiza a lista de perfis"""
    try:
        profiles = detect_edge_profiles()
        socketio.emit('profiles_updated', profiles)
        socketio.emit('log', 'Perfis atualizados com sucesso')
    except Exception as e:
        socketio.emit('log', f'Erro ao atualizar perfis: {str(e)}')

@socketio.on('start_automation')
def handle_start_automation(config):
    """Inicia uma nova automação"""
    try:
        profile_path = config.get('profile')
        if not profile_path:
            socketio.emit('log', 'Perfil não selecionado')
            return
            
        if not os.path.exists(profile_path):
            socketio.emit('log', 'Caminho do perfil não existe')
            return
            
        # Verifica se o caminho do perfil é válido
        if not os.path.isdir(profile_path):
            socketio.emit('log', 'Caminho do perfil inválido')
            return
            
        # Cria uma nova instância de automação
        automation = EdgeAutomation(
            profile_path=profile_path,
            device_type=config.get('deviceType', 'desktop'),
            config={
                'typing_speed': config.get('typingSpeed', 'normal'),
                'min_interval': config.get('minInterval', MIN_SEARCH_INTERVAL),
                'max_interval': config.get('maxInterval', MAX_SEARCH_INTERVAL),
                'click_results': config.get('clickResults', False),
                'click_count': config.get('clickCount', 2),
                'read_time': config.get('readTime', 10),
                'random_scroll': config.get('randomScroll', False)
            }
        )
        
        active_automations[profile_path] = automation
        
        def run_automation():
            try:
                socketio.emit('automation_started')
                automation.start_automation(config.get('searchCount', DEFAULT_SEARCH_COUNT))
            except Exception as e:
                socketio.emit('log', f'Erro durante a automação: {str(e)}')
            finally:
                if profile_path in active_automations:
                    del active_automations[profile_path]
                socketio.emit('automation_stopped')
                
        thread = Thread(target=run_automation)
        thread.daemon = True
        thread.start()
        
    except Exception as e:
        socketio.emit('log', f'Erro ao iniciar automação: {str(e)}')

@socketio.on('stop_automation')
def handle_stop_automation():
    """Para todas as automações em execução"""
    try:
        for automation in active_automations.values():
            automation.stop_automation()
        active_automations.clear()
        socketio.emit('log', 'Automação interrompida com sucesso')
    except Exception as e:
        socketio.emit('log', f'Erro ao parar automação: {str(e)}')

def run_server(host='0.0.0.0', port=5000, debug=False):
    """Inicia o servidor Flask"""
    socketio.run(app, host=host, port=port, debug=debug) 