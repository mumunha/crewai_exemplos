# Projeto de Automação de E-mails

Este projeto é uma ferramenta de automação de e-mails destinada a simplificar o processo de envio e resposta de e-mails para uma equipe ou organização.

## Estrutura do Projeto

O repositório é composto pelos seguintes arquivos e diretórios:

- `main.py`: Arquivo principal que executa o fluxo de automação de e-mails.
- `reply_new_email.py`: Script responsável por responder a novos e-mails recebidos.
- `crew.py`: Módulo que define as funções e classes relacionadas à equipe.
- `config/`: Diretório contendo arquivos de configuração em formato YAML.
  - `agents.yaml`: Arquivo de configuração com informações sobre os agentes de e-mail.
  - `tasks.yaml`: Arquivo de configuração com definições de tarefas e regras de automação.

## Copie os arquivos

Para configurar o projeto, é copiar os arquivos par ao diretorio no qual estao main.py, e agentt.yaml + tasks.yaml para o diretorio config.

## Instale as bibliotecas Google API

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Exemplo de Configuração

seu_email.py.exemplo é um arquivo de exemplo que demonstra como configurar suas credenciais de e-mail para o projeto.
Inclua seu email e renomeie removendo .exemplo, deixando o nome do arquivo como seu_email.py

## Uso

Para executar o script principal, utilize o seguinte comando:

```bash
python reply_new_email.py
```

