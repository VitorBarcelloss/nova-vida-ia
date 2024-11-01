# Projeto Nova Vida

O projeto Nova Vida é um assistente de IA focado em saúde, desenvolvido com Django e ChromaDB. O assistente responde a perguntas relacionadas à saúde e se adapta às preferências do usuário, incluindo o idioma das respostas.

## Inicialização do Projeto

Para iniciar o projeto, siga os passos abaixo:

### Pré-requisitos

- Docker
- Python 3.x

### Configurações Necessárias

Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:

```plaintext
API_KEY=
CHATBOT_MODEL=
CHATBOT_URL=
CHROMA_HOST=
CHROMA_PORT=
```
### Inicialização do Ambiente

1. Instale as dependências do projeto:

   ```bash
   pip install -r requirements.txt
   ```
   
2. Execute o Docker Compose para inicializar os serviços do ChromaDB e Django:

   ```bash
   docker compose up --build
   ```
   O ChromaDB estará disponível na porta 8000 e o Django na porta 8080.

3. Para executar o Streamlit (apenas localmente por enquanto), use o seguinte comando:
   ```bash
   streamlit run app.py
   ```
   O Streamlit estará disponível na porta 8053.
#### Inicialização Local do ChromaDB

Caso queira inicializar o ChromaDB localmente, execute:
```bash
docker run -d -p 8001:8000 chromadb/chroma:0.5.17.dev9
```

#### Observação
Na primeira requisição, pode levar algum tempo, pois a inicialização do ChromaDB depende da instalação de certos modelos no Docker.

### Como Usar

Para enviar uma mensagem ao assistente, faça uma requisição para a seguinte URL:
```
POST localhost:{porta_alocada}/api/chatbot/message
```

#### Exemplo de Body da Requisição

```
{
    "user_msg": "Sua mensagem aqui"
}
```

### Conclusão

Com esta documentação, você deve estar preparado para inicializar e utilizar o projeto Nova Vida. Caso tenha alguma dúvida, consulte a documentação ou entre em contato com o desenvolvedor.