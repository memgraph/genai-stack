from langchain_community.chat_models import ChatOllama
from langchain_community.graphs import MemgraphGraph
from langchain.chains import GraphCypherQAChain
import os

# Set up the connection details from environment variables
URI = os.getenv("NEO4J_URI", "bolt://memgraph:7687")
USER = os.getenv("NEO4J_USER", "")
PASSWORD = os.getenv("NEO4J_PASSWORD", "")


class LlamaHandler:
    def __init__(self):
        self.graph = MemgraphGraph(
            url=URI,
            username=USER,
            password=PASSWORD,
        )

    def get_response(self, question: str):
        chain = GraphCypherQAChain.from_llm(
            ChatOllama(
                temperature=0,
                base_url="http://host.docker.internal:11434",
                model="llama3",
            ),
            graph=self.graph,
            verbose=True,
        )
        try:
            final_answer = chain.invoke(question)
        except Exception as e:
            print(f"Error during chain invocation: {e}")
            final_answer = "Error during chain invocation"
        return final_answer


llama_handler = LlamaHandler()
