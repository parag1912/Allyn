from dotenv import load_dotenv
import os

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.llms import Ollama

# 🔐 Load environment variables (optional, for consistency)
load_dotenv()

# 🗄 Connect to DuckDB (ensure allyin.duckdb is populated)
db = SQLDatabase.from_uri("duckdb:///allyin.duckdb")

# 🧠 Use free local LLM via Ollama
llm = Ollama(model="llama3")

# 🛠 Create the SQL agent
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)

# ❓ Ask your question here
question = "List all customers from New York"
response = agent_executor.invoke({"input": question})

# 📤 Show result
print("\n✅ SQL Agent Response:")
print(response)
