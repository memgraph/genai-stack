from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import MemgraphGraph
from langchain_openai import ChatOpenAI
import os

# Set up the connection details from environment variables
URI = os.getenv("NEO4J_URI", "bolt://memgraph:7687")
USER = os.getenv("NEO4J_USER", "")
PASSWORD = os.getenv("NEO4J_PASSWORD", "")


class GPTHandler:
    def __init__(self):
        self.graph = MemgraphGraph(
            url=URI,
            username=USER,
            password=PASSWORD,
        )

    def get_response(self, question: str):
        chain = GraphCypherQAChain.from_llm(
            ChatOpenAI(temperature=0),
            graph=self.graph,
            verbose=True,
            model_name="gpt-4",
        )
        try:
            response = chain.invoke(question)
            print(f"Chain result: {response}")
            # Extract the final answer from the result
            final_answer = response.get("result", "No answer found")
            print(final_answer)
        except Exception as e:
            print(f"Error during chain invocation: {e}")
            final_answer = "Error during chain invocation"
        return final_answer


gpt_handler = GPTHandler()
