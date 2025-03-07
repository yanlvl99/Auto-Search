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

### Instalação
1. Clone o repositório:
```bash
git clone [url-do-repositorio]
cd auto-search
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:
```bash
python -m src.auto_search
```

### Configuração
1. Abra o aplicativo no navegador (geralmente em `http://localhost:5000`)
2. Selecione o perfil do Edge desejado
3. Configure as opções de automação:
   - Número de pesquisas
   - Tipo de dispositivo (desktop/mobile)
   - Velocidade de digitação
   - Intervalo entre pesquisas
   - Comportamento de cliques

## ⚙️ Configurações Avançadas

### Perfis
- O sistema detecta automaticamente os perfis do Edge instalados
- Suporta perfis padrão e personalizados
- Mantém cookies e dados de login

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

### Problemas Comuns
1. **Perfil não carrega**
   - Verifique se o Edge está fechado
   - Certifique-se de que o perfil existe
   - Tente atualizar a lista de perfis

2. **Automação trava**
   - Clique no botão "Parar"
   - Aguarde a limpeza dos recursos
   - Reinicie o aplicativo

3. **Conta desconecta**
   - Verifique se o perfil está corretamente selecionado
   - Certifique-se de que o Edge não está em uso
   - Tente fazer login manualmente primeiro

## 📝 Notas
- Recomenda-se não usar o Edge durante a automação
- Mantenha o sistema atualizado
- Use intervalos razoáveis entre pesquisas
- Evite números excessivos de pesquisas

## ⚠️ Aviso Legal
Este software é para fins educacionais e de automação pessoal. O uso deve estar em conformidade com os termos de serviço do Bing e Microsoft Edge.

## 🤝 Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

## 📄 Licença
Este projeto está licenciado sob a [MIT License](LICENSE) 