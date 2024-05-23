# Memgraph GenAI Stack
**Docker Compose + FastAPI + LangChain + Ollama/OpenAI + Memgraph**

This demo is a template for building GenAI applications with Memgraph.

## Start the app

To chat with Memgraph via OpenAI, create the `.env` file in the root directory and set your OpenAI API key:
```
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

Run the app:
```
docker compose up
```

A dataset needs to be loaded in Memgraph before the backend is started in order for schema to be generated. The Game of Thrones dataset is preloaded in this demo. 

This demo offers querying Memgraph with natural language via LangChain utilizing two different models:

- [OpenAI GPT-4](#ask-memgraph-with-gpt-4)
- [Ollama Llama 3](#ask-memgraph-with-llama-3)

## Ask Memgraph with GPT-4

Ask Memgraph with OpenAI GPT-4 model:
```
curl -X POST "http://localhost:8000/ask/openai" -H "Content-Type: application/json" -d '{"question": "How many seasons there are?"}'
```

Here is the response:
```
{"question":"How many seasons there are?","response":"There are 8 seasons."}%  
```

## Ask Memgraph with Llama 3

Ask Memgraph with Llama3 model:
```
curl -X POST "http://localhost:8000/ask/ollama" -H "Content-Type: application/json" -d '{"question": "How many seasons there are?"}'         
```

Here is the response:
```
{"question":"How many seasons there are?","response":"There are 8 seasons."}% 
```
