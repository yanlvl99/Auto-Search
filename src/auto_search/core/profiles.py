import os
import json
import logging
from typing import List, Dict
from ..config.settings import EDGE_PROFILES_PATH

logger = logging.getLogger(__name__)

def detect_edge_profiles() -> List[Dict[str, str]]:
    """Detecta os perfis do Microsoft Edge instalados no sistema."""
    profiles = []
    
    try:
        if not os.path.exists(EDGE_PROFILES_PATH):
            logger.warning(f"Caminho de perfis não encontrado: {EDGE_PROFILES_PATH}")
            return profiles
            
        # Procura por pastas de perfil (Default, Profile 1, Profile 2, etc.)
        for item in os.listdir(EDGE_PROFILES_PATH):
            profile_path = os.path.join(EDGE_PROFILES_PATH, item)
            preferences_path = os.path.join(profile_path, 'Preferences')
            
            # Verifica se é um diretório de perfil válido
            if not os.path.isdir(profile_path):
                continue
                
            # Verifica se tem o arquivo Preferences
            if not os.path.exists(preferences_path):
                continue
                
            try:
                with open(preferences_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Tenta obter o nome do perfil de diferentes locais no arquivo
                profile_name = None
                if 'profile' in data:
                    profile_name = data['profile'].get('name')
                elif 'account_info' in data:
                    profile_name = data['account_info'].get('full_name')
                elif 'gaia_info' in data:
                    profile_name = data['gaia_info'].get('full_name')
                
                # Se não encontrou nome, usa o nome da pasta
                if not profile_name:
                    profile_name = "Perfil " + item if item != "Default" else "Perfil Padrão"
                    
                # Adiciona o perfil à lista com o caminho completo
                profiles.append({
                    'name': profile_name,
                    'path': profile_path,
                    'profile_id': item
                })
                logger.info(f"Perfil detectado: {profile_name} em {profile_path}")
                
            except json.JSONDecodeError as e:
                logger.error(f"Erro ao ler arquivo de preferências do perfil {item}: {str(e)}")
                continue
            except Exception as e:
                logger.error(f"Erro ao processar perfil {item}: {str(e)}")
                continue
    
    except Exception as e:
        logger.error(f"Erro ao detectar perfis: {str(e)}")
        
    return sorted(profiles, key=lambda x: x['name'])

def get_profile_path(profile_id: str) -> str:
    """Retorna o caminho completo para um perfil específico."""
    if not profile_id:
        return EDGE_PROFILES_PATH
        
    return os.path.join(EDGE_PROFILES_PATH, profile_id) 