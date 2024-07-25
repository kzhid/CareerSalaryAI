import os
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms import Ollama
from llama_index.agent import ReActAgent

# Initialize Ollama with the Llama 3 model
llm = Ollama(model="llama3")

# Load documents from a directory (adjust the path as needed)
documents = SimpleDirectoryReader('data').load_data()

# Create a vector store index
index = VectorStoreIndex.from_documents(documents)

# Create a query engine
query_engine = index.as_query_engine()

# Initialize the ReAct agent
agent = ReActAgent.from_tools(
    [query_engine],
    llm=llm,
    verbose=True
)

# Example usage
response = agent.chat("What information can you provide about career salaries?")
print(response)
