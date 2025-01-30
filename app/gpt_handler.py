from langchain_community.chains.graph_qa.memgraph import MemgraphQAChain
from langchain_community.graphs import MemgraphGraph
from langchain_openai import ChatOpenAI
import os

# Set up the connection details from environment variables
url = os.environ.get("MEMGRAPH_URI", "bolt://memgraph:7687")
username = os.environ.get("MEMGRAPH_USERNAME", "")
password = os.environ.get("MEMGRAPH_PASSWORD", "")


class GPTHandler:
    def __init__(self):
        self.graph = MemgraphGraph(
            url=url, username=username, password=password, refresh_schema=False
        )

    def get_response(self, question: str):
        chain = MemgraphQAChain.from_llm(
            ChatOpenAI(temperature=0),
            graph=self.graph,
            verbose=True,
            model_name="gpt-4",
            allow_dangerous_requests=True,
        )

        try:
            response = chain.invoke(question).get("result", "No answer found")
        except Exception as e:
            print(f"Error during chain invocation: {e}")
            response = "Error during chain invocation"
        return response


gpt_handler = GPTHandler()
