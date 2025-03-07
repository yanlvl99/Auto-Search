# Auto Search - Automação Bing

Automatize suas pesquisas no Bing de forma inteligente e segura.

## 📋 Requisitos

- Windows 10 ou superior
- Python 3.8 ou superior
- Microsoft Edge instalado
- Conta Microsoft (para pontos rewards)

## 🚀 Instalação

### Método 1: Com Git

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/auto-search.git
cd auto-search
```

2. Execute o arquivo `iniciar.bat`
   - O script irá criar um ambiente virtual
   - Instalará todas as dependências necessárias
   - Iniciará o servidor automaticamente

### Método 2: Sem Git (Download direto)

1. Baixe o projeto:
   - Acesse a página do projeto no GitHub
   - Clique no botão verde "Code"
   - Selecione "Download ZIP"
   - Extraia o arquivo ZIP para uma pasta de sua preferência

2. Execute o arquivo `iniciar.bat`
   - O script irá criar um ambiente virtual
   - Instalará todas as dependências necessárias
   - Iniciará o servidor automaticamente

### Configuração do Inicialização Automática (Opcional)

1. Crie um atalho do `iniciar.bat` nesta pasta:
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