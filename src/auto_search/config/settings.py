import os
import platform
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Any
import random

# Carregar variáveis de ambiente
load_dotenv()

# Configurações básicas
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Configurações do Edge
def get_edge_profiles_path():
    system = platform.system()
    user_home = str(Path.home())
    
    if system == 'Windows':
        return os.path.join(user_home, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data')
    elif system == 'Linux':
        return os.path.join(user_home, '.config', 'microsoft-edge')
    elif system == 'Darwin':  # macOS
        return os.path.join(user_home, 'Library', 'Application Support', 'Microsoft Edge')
    return ''

EDGE_PROFILES_PATH = os.getenv('EDGE_PROFILES_PATH', get_edge_profiles_path())
DEFAULT_SEARCH_COUNT = 30
MIN_SEARCH_INTERVAL = 2  # segundos
MAX_SEARCH_INTERVAL = 5  # segundos

# Configurações de digitação
TYPING_SPEEDS: Dict[str, float] = {
    'instant': 0,
    'fast': 0.05,
    'normal': 0.1, 
    'slow': 0.2
}

# Configurações de navegação
DEFAULT_CLICK_COUNT = 2
DEFAULT_READ_TIME = 10  # segundos
SCROLL_PROBABILITY = 0.7

# Configurações de pesquisa
SEARCH_TERMS: List[str] = [
    "notícias hoje",
    "previsão do tempo",
    "receitas fáceis",
    "filmes em cartaz",
    "jogos online",
    "música popular",
    "esportes ao vivo",
    "tecnologia novidades",
    "saúde e bem-estar",
    "viagens brasil",
    "educação online",
    "empregos disponíveis",
    "compras online",
    "dicas de decoração",
    "exercícios em casa",
    "carros novos",
    "moda tendências",
    "restaurantes próximos",
    "eventos culturais",
    "cursos gratuitos"
]

# Configurações de logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'logs', 'auto_search.log')

# Configurar logging
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Configurações de arquivos
PROFILES_FILE = 'profiles.json'
STATS_FILE = 'stats.json'
PRESETS_FILE = 'presets.json'

# User Agents
MOBILE_USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 12; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 EdgA/120.0.0.0",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 EdgA/120.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 EdgiOS/120.0.0.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 EdgA/120.0.0.0",
    "Mozilla/5.0 (Linux; Android 12; motorola edge 30 ultra) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 EdgA/120.0.0.0"
]

DESKTOP_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
]

# Configurações do Edge
EDGE_CAPABILITIES = {
    "ms:edgeOptions": {
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--disable-features=msEdgeAdsBlockerOnAllowed",
            "--disable-features=msEdgeCollectionsSync",
            "--disable-features=msEdgeDiscoverFeed",
            "--disable-features=msEdgeFollowButton",
            "--disable-features=msEdgeNewTabPageContentDiscovery",
            "--disable-features=msEdgeNewTabPageLayout",
            "--disable-features=msEdgePasswordManager",
            "--disable-features=msEdgeShoppingAssist",
            "--disable-features=msEdgeSidebarV2",
            "--disable-features=msEdgeSync",
            "--disable-features=msEdgeSystemExtensions",
            "--disable-features=msEdgeWebWidget",
            "--disable-features=msOmniboxDynamicMaxAutocomplete",
            "--disable-features=msOmniboxUIExperimentalSuggestionRanking",
            "--disable-features=msReadAloud",
            "--disable-features=msSmartScreen",
            "--disable-features=msWebAssistant"
        ],
        "prefs": {
            "profile.default_content_settings.popups": 0,
            "profile.default_content_settings.notifications": 2,
            "profile.password_manager_enabled": False,
            "credentials_enable_service": False,
            "profile.default_content_setting_values.media_stream_mic": 2,
            "profile.default_content_setting_values.media_stream_camera": 2,
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2
        }
    }
}

# Seleciona um User Agent aleatório baseado no tipo de dispositivo
MOBILE_USER_AGENT = random.choice(MOBILE_USER_AGENTS)
DESKTOP_USER_AGENT = random.choice(DESKTOP_USER_AGENTS) 