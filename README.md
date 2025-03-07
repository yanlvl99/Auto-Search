# Auto Search - Automação de Pesquisas Bing

## 📋 Descrição
Auto Search é uma ferramenta de automação para realizar pesquisas no Bing de forma inteligente e segura. O sistema simula comportamento humano e suporta múltiplos perfis do Microsoft Edge.

## ✨ Funcionalidades
- 🔄 Automação de pesquisas no Bing
- 👥 Suporte a múltiplos perfis do Edge
- 🎭 Simulação de comportamento humano
- 📱 Suporte para pesquisas desktop e mobile
- 🔒 Preservação de login e cookies
- 🎯 Cliques aleatórios em resultados
- ⚡ Velocidade de digitação configurável
- 🕒 Intervalos aleatórios entre pesquisas

## 🚀 Como Usar

### Pré-requisitos
- Python 3.8 ou superior
- Microsoft Edge instalado
- Pip (gerenciador de pacotes Python)

### Instalação no Windows

1. Baixe o arquivo ZIP do projeto
2. Extraia em uma pasta de sua preferência (exemplo: `C:\Auto Search`)
3. Dê dois cliques no arquivo `iniciar.bat`

### Configuração do iniciar.bat
O arquivo `iniciar.bat` é um script que facilita a execução do programa no Windows. Para configurá-lo:

1. Clique com o botão direito no arquivo `iniciar.bat`
2. Selecione "Editar"
3. Configure as variáveis conforme necessário:
```batch
@echo off
:: Configurações do ambiente
set PYTHON_PATH=python
set VENV_NAME=.venv
set HOST=localhost
set PORT=5000

:: Não altere as linhas abaixo a menos que saiba o que está fazendo
if not exist "%VENV_NAME%" (
    echo Criando ambiente virtual...
    %PYTHON_PATH% -m venv %VENV_NAME%
)

:: Ativa o ambiente virtual
call %VENV_NAME%\Scripts\activate

:: Instala/atualiza dependências
pip install -r requirements.txt

:: Inicia a aplicação
python -m src.auto_search
```

### Executando Automaticamente com o Windows

Para fazer o programa iniciar junto com o Windows:

1. Pressione `Windows + R`
2. Digite `shell:startup`
3. Crie um atalho do `iniciar.bat` nesta pasta:
   - Clique com botão direito no `iniciar.bat`
   - Selecione "Criar atalho"
   - Mova o atalho para a pasta Startup

### Configuração da Interface
1. Abra o aplicativo no navegador (geralmente em `http://localhost:5000`)
2. Selecione o perfil do Edge desejado
3. Configure as opções de automação:
   - Número de pesquisas
   - Tipo de dispositivo (desktop/mobile)
   - Velocidade de digitação
   - Intervalo entre pesquisas
   - Comportamento de cliques

## ⚙️ Configurações Avançadas

### Perfis do Edge
- Localização padrão dos perfis no Windows:
  ```
  C:\Users\[SEU-USUARIO]\AppData\Local\Microsoft\Edge\User Data
  ```
- Perfis comuns:
  - Default (Padrão)
  - Profile 1
  - Profile 2
  - etc.

### Comportamento
- Simulação de movimentos do mouse
- Scroll aleatório nas páginas
- Cliques em resultados aleatórios
- Tempo de leitura variável
- Intervalos dinâmicos entre ações

## 🛡️ Segurança
- Execução em perfil isolado
- Proteção contra detecção de automação
- Limpeza automática de recursos temporários
- Gerenciamento seguro de sessões

## 🔍 Solução de Problemas

### Problemas Comuns no Windows

1. **iniciar.bat não funciona**
   - Verifique se o Python está instalado corretamente
   - Verifique se o Python está nas variáveis de ambiente do Windows
   - Execute o comando `python --version` no cmd para confirmar

2. **Perfil não carrega**
   - Feche TODAS as janelas do Edge
   - Verifique o Gerenciador de Tarefas e encerre processos do Edge
   - Certifique-se de que o caminho do perfil está correto

3. **Erro de permissão**
   - Execute o iniciar.bat como administrador
   - Verifique as permissões da pasta do projeto
   - Certifique-se de que o antivírus não está bloqueando

4. **Porta em uso**
   - Altere a porta no iniciar.bat (PORT=5000 para outro número)
   - Verifique se não há outra instância rodando
   - Feche outros programas que possam usar a mesma porta

## 📝 Notas Importantes
- Recomenda-se não usar o Edge durante a automação
- Mantenha o sistema e o Python atualizados
- Use intervalos razoáveis entre pesquisas
- Evite números excessivos de pesquisas
- Faça backup dos seus perfis do Edge regularmente

## ⚠️ Aviso Legal
Este software é para fins educacionais e de automação pessoal. O uso deve estar em conformidade com os termos de serviço do Bing e Microsoft Edge.

## 🤝 Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

## 📄 Licença
Este projeto está licenciado sob a [MIT License](LICENSE) 