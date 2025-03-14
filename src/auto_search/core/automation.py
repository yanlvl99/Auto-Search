import os
import time
import random
import logging
import shutil
import tempfile
import uuid
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from ..config.settings import (
    MOBILE_USER_AGENTS,
    DESKTOP_USER_AGENTS,
    DEFAULT_SEARCH_COUNT,
    MIN_SEARCH_INTERVAL,
    MAX_SEARCH_INTERVAL,
    SEARCH_TERMS
)

logger = logging.getLogger(__name__)

class EdgeAutomation:
    def __init__(self, profile_path: str, device_type: str = 'desktop', config: Optional[Dict[str, Any]] = None):
        """
        Inicializa a automação do Edge
        
        Args:
            profile_path: Caminho para o perfil do Edge
            device_type: Tipo de dispositivo ('desktop' ou 'mobile')
            config: Configurações adicionais
        """
        self.profile_path = profile_path
        self.device_type = device_type
        self.driver = None
        self.is_running = False
        
        # Configurações padrão
        self.config = config or {}
        self.typing_speed = self.config.get('typing_speed', 'normal')
        self.click_results = self.config.get('click_results', False)
        self.click_count = self.config.get('click_count', 2)
        self.read_time = self.config.get('read_time', 10)
        self.min_interval = self.config.get('min_interval', MIN_SEARCH_INTERVAL)
        self.max_interval = self.config.get('max_interval', MAX_SEARCH_INTERVAL)
        self.min_typing_delay = self.config.get('min_typing_delay', 0.1)
        self.max_typing_delay = self.config.get('max_typing_delay', 0.3)
        self.click_random_results_prob = self.config.get('click_random_results_prob', 0.7)
        self.use_custom_terms = self.config.get('use_custom_terms', False)
        self.custom_terms = self.config.get('custom_terms', [])
        self.random_scroll = self.config.get('random_scroll', False)
        
        # Sobrescrever configurações padrão com as fornecidas
        if config:
            for key, value in config.items():
                if hasattr(self, key):
                    setattr(self, key, value)
        
    def setup_driver(self):
        """Configura e inicializa o driver do Edge com configurações anti-detecção"""
        try:
            options = Options()
            
            # Gera um ID único para a sessão
            session_id = str(uuid.uuid4())[:8]
            temp_dir = os.path.join(tempfile.gettempdir(), f'edge_automation_{session_id}')
            
            # Cria o diretório temporário
            os.makedirs(temp_dir, exist_ok=True)
            
            # Copia apenas os arquivos necessários do perfil original
            profile_name = os.path.basename(self.profile_path)
            temp_profile_dir = os.path.join(temp_dir, profile_name)
            
            # Lista de arquivos/pastas importantes para copiar
            important_items = [
                'Preferences',
                'Cookies',
                'Login Data',
                'Web Data',
                'Network',
                'Local Storage',
                'Extension State',
                'Sync Data',
                'Sessions',
                'Accounts'
            ]
            
            try:
                os.makedirs(temp_profile_dir, exist_ok=True)
                
                # Primeiro, tenta copiar todo o perfil
                try:
                    shutil.copytree(self.profile_path, temp_profile_dir, dirs_exist_ok=True)
                    logger.info("Perfil copiado com sucesso")
                except Exception as e:
                    logger.warning(f"Erro ao copiar perfil completo, tentando copiar arquivos importantes: {str(e)}")
                    # Se falhar, tenta copiar apenas os arquivos importantes
                    for item in important_items:
                        src = os.path.join(self.profile_path, item)
                        dst = os.path.join(temp_profile_dir, item)
                        if os.path.exists(src):
                            try:
                                if os.path.isfile(src):
                                    shutil.copy2(src, dst)
                                elif os.path.isdir(src):
                                    shutil.copytree(src, dst, dirs_exist_ok=True)
                            except Exception as e:
                                logger.warning(f"Erro ao copiar {item}: {str(e)}")
                                continue
                
            except Exception as e:
                logger.warning(f"Erro ao copiar arquivos do perfil: {str(e)}")
            
            # Configura o Edge para usar o diretório temporário
            options.add_argument(f'--user-data-dir={temp_dir}')
            if profile_name != "Default":
                options.add_argument(f'--profile-directory={profile_name}')
            
            logger.info(f"Usando diretório temporário: {temp_dir}")
            logger.info(f"Perfil selecionado: {profile_name}")
            
            # Armazena o caminho temporário para limpeza posterior
            self.temp_dir = temp_dir
            
            # Configurações adicionais
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-default-apps')
            options.add_argument('--no-first-run')
            options.add_argument('--no-default-browser-check')
            options.add_argument('--start-maximized')
            options.add_argument('--window-size=1920,1080')
            
            # Configurações experimentais
            options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Configurar User Agent aleatório
            user_agents = MOBILE_USER_AGENTS if self.device_type == 'mobile' else DESKTOP_USER_AGENTS
            options.add_argument(f'user-agent={random.choice(user_agents)}')
            
            service = Service(EdgeChromiumDriverManager().install())
            self.driver = webdriver.Edge(service=service, options=options)
            
            # Remover flags de automação
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    delete navigator.__proto__.webdriver;
                '''
            })
            
            # Configurar cookies do Bing
            self.driver.get("https://www.bing.com")
            time.sleep(random.uniform(1, 2))
            
        except Exception as e:
            # Limpa o diretório temporário em caso de erro
            self._cleanup_temp_dir()
            logger.error(f"Erro ao configurar driver: {str(e)}")
            raise
            
    def _cleanup_temp_dir(self):
        """Limpa o diretório temporário"""
        if hasattr(self, 'temp_dir') and self.temp_dir and os.path.exists(self.temp_dir):
            try:
                # Tenta remover o diretório várias vezes com pequenos intervalos
                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        shutil.rmtree(self.temp_dir, ignore_errors=True)
                        if not os.path.exists(self.temp_dir):
                            logger.info(f"Diretório temporário removido: {self.temp_dir}")
                            break
                        time.sleep(1)  # Aguarda um pouco antes de tentar novamente
                    except Exception as e:
                        if attempt == max_attempts - 1:  # Última tentativa
                            logger.error(f"Erro ao remover diretório temporário após {max_attempts} tentativas: {str(e)}")
                        else:
                            logger.warning(f"Tentativa {attempt + 1} falhou ao remover diretório temporário: {str(e)}")
            except Exception as e:
                logger.error(f"Erro ao remover diretório temporário: {str(e)}")
                
    def _get_typing_delay(self) -> float:
        """Retorna o delay de digitação baseado na velocidade configurada"""
        delays = {
            'instant': 0,
            'fast': 0.05,
            'normal': 0.1,
            'slow': 0.2
        }
        return delays.get(self.typing_speed, 0.05)

    def _type_like_human(self, element, text: str):
        """Simula digitação humana com velocidade configurável"""
        delay = self._get_typing_delay()
        if delay == 0:  # Digitação instantânea
            element.send_keys(text)
        else:
            for char in text:
                element.send_keys(char)
                time.sleep(random.uniform(delay * 0.8, delay * 1.2))

    def _simulate_human_behavior(self):
        """Simula comportamento humano aleatório"""
        if self.random_scroll:
            # Scroll aleatório
            for _ in range(random.randint(1, 3)):
                scroll_amount = random.randint(100, 800)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(0.5, 1.5))
                
                # Chance de scroll para cima
                if random.random() < 0.3:
                    scroll_up = random.randint(50, scroll_amount)
                    self.driver.execute_script(f"window.scrollBy(0, -{scroll_up});")
                    time.sleep(random.uniform(0.3, 0.8))

        # Movimento do mouse (simulado)
        self.driver.execute_script("""
            var event = new MouseEvent('mousemove', {
                'view': window,
                'bubbles': true,
                'cancelable': true,
                'clientX': arguments[0],
                'clientY': arguments[1]
            });
            document.dispatchEvent(event);
        """, random.randint(0, 800), random.randint(0, 600))

    def _click_random_results(self):
        """Clica em resultados aleatórios da pesquisa"""
        if not self.click_results:
            return

        try:
            # Encontra todos os resultados
            results = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#b_results h2 a"))
            )

            # Seleciona resultados aleatórios para clicar
            clicks = min(self.click_count, len(results))
            selected_results = random.sample(results, clicks)

            main_window = self.driver.current_window_handle

            for result in selected_results:
                try:
                    if not self.is_running:
                        return

                    # Scroll até o resultado
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", result)
                    time.sleep(random.uniform(0.5, 1))

                    # Abre o link em nova aba
                    self.driver.execute_script("window.open(arguments[0].href, '_blank');", result)
                    time.sleep(1)

                    # Muda para a nova aba
                    new_window = self.driver.window_handles[-1]
                    self.driver.switch_to.window(new_window)

                    # Simula leitura da página
                    self._simulate_human_behavior()
                    time.sleep(random.uniform(self.read_time * 0.8, self.read_time * 1.2))

                    # Fecha a aba atual
                    self.driver.close()

                    # Volta para a aba principal
                    self.driver.switch_to.window(main_window)

                except Exception as e:
                    logger.warning(f"Erro ao processar resultado: {str(e)}")
                    # Garante que voltamos para a janela principal em caso de erro
                    try:
                        self.driver.switch_to.window(main_window)
                    except:
                        pass
                    continue

        except Exception as e:
            logger.error(f"Erro ao interagir com resultados: {str(e)}")
            # Tenta recuperar a janela principal
            try:
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                pass

    def perform_search(self, search_term: str):
        """Realiza uma única pesquisa simulando comportamento humano"""
        if not self.is_running:
            return False

        try:
            # Abre o Bing
            self.driver.get("https://www.bing.com")
            if not self.is_running:
                return False
            time.sleep(random.uniform(1, 2))
            
            # Encontra o campo de pesquisa
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            if not self.is_running:
                return False
                
            # Limpa o campo e digita como humano
            search_box.clear()
            self._type_like_human(search_box, search_term)
            
            if not self.is_running:
                return False
                
            # Simula comportamento antes de pesquisar
            self._simulate_human_behavior()
            
            if not self.is_running:
                return False
                
            # Pressiona Enter
            search_box.send_keys(Keys.RETURN)
            
            # Aguarda resultados e simula leitura
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "b_results"))
            )
            
            if not self.is_running:
                return False
                
            # Simula leitura dos resultados e clica em alguns
            self._simulate_human_behavior()
            
            if self.is_running:
                self._click_random_results()
            
            return True
        except Exception as e:
            logger.error(f"Erro na pesquisa '{search_term}': {str(e)}")
            # Tenta recuperar em caso de erro
            try:
                if self.driver.window_handles:
                    self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                pass
            return False

    def start_automation(self, search_count: int = DEFAULT_SEARCH_COUNT):
        """Inicia o processo de automação"""
        try:
            self.setup_driver()
            self.is_running = True
            
            searches_completed = 0
            termos_usados = set()

            while searches_completed < search_count and self.is_running:
                # Gera uma pergunta natural usando templates
                import random
                from ..config.settings import SEARCH_TERMS

                # Templates de perguntas comuns
                templates_perguntas = [
                    "Como fazer {}?",
                    "Qual é a melhor maneira de {}?",
                    "O que significa {}?",
                    "Onde encontrar {}?",
                    "Quais são os benefícios de {}?",
                    "Por que {} acontece?",
                    "Quando devo {}?",
                    "Como funciona {}?",
                    "Qual a diferença entre {} e {}?",
                    "Como resolver problemas com {}?"
                ]

                # Tópicos comuns para gerar perguntas relevantes
                topicos = [
                    "exercícios", "meditação", "alimentação saudável", "sono", "produtividade",
                    "estudo", "trabalho remoto", "investimentos", "programação", "idiomas",
                    "jardinagem", "culinária", "fotografia", "música", "arte",
                    "viagem", "tecnologia", "saúde", "bem-estar", "sustentabilidade",
                    "reciclagem", "energia renovável", "marketing digital", "redes sociais",
                    "desenvolvimento pessoal", "carreira", "finanças pessoais", "decoração",
                    "organização", "limpeza", "manutenção", "consertos", "DIY"
                ]

                # Gera uma pergunta aleatória
                if random.random() > 0.3 and SEARCH_TERMS:  # 30% de chance de usar termos personalizados
                    search_term = random.choice(SEARCH_TERMS)
                else:
                    template = random.choice(templates_perguntas)
                    if "{}" in template:
                        if template.count("{}") == 2:
                            # Para templates que precisam de dois tópicos
                            topicos_selecionados = random.sample(topicos, 2)
                            search_term = template.format(topicos_selecionados[0], topicos_selecionados[1])
                        else:
                            # Para templates que precisam de um tópico
                            topico = random.choice(topicos)
                            search_term = template.format(topico)
                
                # Se o termo já foi usado, gerar outro
                while search_term in termos_usados:
                    if random.random() > 0.3 and SEARCH_TERMS:
                        search_term = random.choice(SEARCH_TERMS)
                    else:
                        template = random.choice(templates_perguntas)
                        if "{}" in template:
                            if template.count("{}") == 2:
                                topicos_selecionados = random.sample(topicos, 2)
                                search_term = template.format(topicos_selecionados[0], topicos_selecionados[1])
                            else:
                                topico = random.choice(topicos)
                                search_term = template.format(topico)
                
                termos_usados.add(search_term)
                
                if self.perform_search(search_term):
                    searches_completed += 1
                    logger.info(f"Pesquisa {searches_completed}/{search_count} realizada: {search_term}")
                    
                    # Intervalo aleatório entre pesquisas
                    if searches_completed < search_count:
                        delay = random.uniform(self.min_interval, self.max_interval)
                        time.sleep(delay)
                        
        except Exception as e:
            logger.error(f"Erro durante a automação: {str(e)}")
        finally:
            self.stop_automation()
            
    def stop_automation(self):
        """Para o processo de automação e limpa recursos"""
        logger.info("Iniciando parada da automação...")
        
        # Marca como não executando primeiro
        self.is_running = False
        
        # Tenta fechar o navegador com segurança
        if self.driver:
            try:
                # Lista todas as janelas antes de começar a fechar
                all_handles = self.driver.window_handles
                logger.info(f"Fechando {len(all_handles)} janelas")
                
                # Se tiver mais de uma janela, tenta fechar uma por uma
                if len(all_handles) > 1:
                    # Guarda a janela principal
                    main_window = self.driver.current_window_handle
                    
                    for handle in all_handles:
                        if handle != main_window:
                            try:
                                self.driver.switch_to.window(handle)
                                self.driver.close()
                                logger.info(f"Janela fechada: {handle}")
                            except Exception as e:
                                logger.warning(f"Erro ao fechar janela {handle}: {str(e)}")
                    
                    # Volta para a janela principal
                    try:
                        self.driver.switch_to.window(main_window)
                    except Exception as e:
                        logger.warning(f"Erro ao voltar para janela principal: {str(e)}")
                
                # Tenta fechar apenas a janela atual do navegador
                try:
                    self.driver.quit()
                    logger.info("Navegador fechado normalmente")
                except Exception as e:
                    logger.warning(f"Erro ao fechar navegador normalmente: {str(e)}")
                
            except Exception as e:
                logger.error(f"Erro durante o processo de parada: {str(e)}")
            finally:
                self.driver = None
        
        # Limpa o diretório temporário
        try:
            self._cleanup_temp_dir()
        except Exception as e:
            logger.error(f"Erro ao limpar diretório temporário: {str(e)}")
        
        logger.info("Automação parada com sucesso") 