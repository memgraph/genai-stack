from langchain_ollama import ChatOllama
from langchain_community.chains.graph_qa.memgraph import MemgraphQAChain
from langchain_community.graphs import MemgraphGraph
import os


# Set up the connection details from environment variables
url = os.environ.get("MEMGRAPH_URI", "bolt://memgraph:7687")
username = os.environ.get("MEMGRAPH_USERNAME", "")
password = os.environ.get("MEMGRAPH_PASSWORD", "")


class LlamaHandler:
    def __init__(self):
        self.graph = MemgraphGraph(
            url=url, username=username, password=password, refresh_schema=False
        )

    def get_response(self, question: str):
        chain = MemgraphQAChain.from_llm(
            ChatOllama(
                temperature=0,
                base_url="http://host.docker.internal:11434",
                model="llama3",
            ),
            graph=self.graph,
            verbose=True,
            allow_dangerous_requests=True,
        )
        try:
            final_answer = chain.invoke(question)
        except Exception as e:
            print(f"Error during chain invocation: {e}")
            final_answer = "Error during chain invocation"
        return final_answer


llama_handler = LlamaHandler()
