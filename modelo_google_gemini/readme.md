# Configuração do Modelo Gemini da Google

Este guia fornece as etapas necessárias para configurar o modelo Gemini da Google no seu projeto.


Assista o vídeo para ver as instruções detalhadas



## Gerar API Key

1. Acesse o console do Gemini da Google- [link](https://aistudio.google.com/app/apikey).
2. Gere uma nova API key.

## Configurar o Ambiente

Adicione a chave gerada ao seu arquivo `.env`:

```
GOOGLE_API_KEY="sua_chave_aqui"
```

## Atualizar Dependências

Adicione as seguintes linhas no seu arquivo `pyproject.toml` para incluir as dependências necessárias na categoria `[tool.poetry.dependencies]`:

```toml
[tool.poetry.dependencies]
...
langchain_google_genai = "1.0.3"
google-generativeai = "0.5.2"
```

## Rodar os comandos poetry para atualizar as dependências


```python
poetry lock
poetry install
```


## Modificar o Arquivo crew.py

Adicione o seguinte código no arquivo `crew.py` para configurar e inicializar o modelo:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Carrega a API key do arquivo .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Cria uma instância do modelo Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    verbose=True,
    temperature=0.5,
    google_api_key=GOOGLE_API_KEY
)
```

em todos os agentes que você tiver na sua equipe, adicione a linha `llm=llm` conforme exemplo abaixo:

```python
	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True,
			llm=llm
		)
```

no lugar do gemini-pro vc pode usar outros modelos, ver no link:

[Modelos Google Gemini AI](https://ai.google.dev/gemini-api/docs/models/gemini?_gl=1*rl8r70*_up*MQ..&gclid=Cj0KCQjw0MexBhD3ARIsAEI3WHLJXCRaDAbqzrbde8bZi_t_ZFwmzFwUlq-NYzYdrYbThJxYTLlp0KQaAgNwEALw_wcB#model-variations)



## Próximos Passos

Após completar as configurações acima, você pode executar o comando de python para rodar a crew - exemplo:

```python
poetry run agencia_noticias "noticias sobre robocop"
```


