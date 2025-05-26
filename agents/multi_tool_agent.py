import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

from langchain_community.utilities import SQLDatabase
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Qdrant

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from neo4j import GraphDatabase

# Load environment variables
load_dotenv()

# 🧠 Local LLM
llm = Ollama(
    model="llama3",
    system="Always return a clear and concise final answer after the result. Do not keep repeating the same query. Stop reasoning after giving your answer."
)

# 🔹 SQL Tool
db = SQLDatabase.from_uri("duckdb:///allyin.duckdb")

def sql_tool_fn(query: str) -> str:
    try:
        # Remove wrapping quotes if present (e.g., "'SELECT ...'")
        if query.startswith("'") and query.endswith("'"):
            query = query[1:-1]
        return db.run(query)
    except Exception as e:
        return f"⚠️ SQL Error: {str(e)}"


sql_tool = Tool(
    name="sql_query_tool",
    func=sql_tool_fn,
    description=(
        "Use for SQL-style queries on structured company data.\n"
        "Available tables: customers (customer_id, name, location), orders (order_id, customer_id, amount).\n"
        "Use correct SQL syntax like: SELECT * FROM customers WHERE location = 'New York';"
    )
)



# 🔹 Vector Tool
model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant_client = QdrantClient(host="localhost", port=6333)

def vector_tool_fn(query: str) -> str:
    vector = model.encode(query).tolist()
    results = qdrant_client.search("docs", query_vector=vector, limit=3)
    return "\n\n".join([
        f"📄 {r.payload.get('source')}:\n{r.payload.get('content')[:300]}..." for r in results
    ])

vector_tool = Tool(
    name="semantic_search",
    func=vector_tool_fn,
    description="Use to search over unstructured content like PDFs and emails"
)

# 🔹 Graph Tool (single string input)
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test1234"))

def graph_tool_fn(_query: str) -> str:
    with driver.session() as session:
        results = session.run("""
            MATCH (f:Facility)-[:EXCEEDS]->(r:Regulation)
            RETURN f.name AS facility, r.type AS regulation
        """)
        return "\n".join([
            f"{r['facility']} exceeds {r['regulation']}" for r in results
        ])

graph_tool = Tool(
    name="graph_tool",
    func=graph_tool_fn,
    description="Use to answer questions about facilities and regulations using a graph database like Neo4j"
)

# 🚀 Initialize agent
tools = [sql_tool, vector_tool, graph_tool]


agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

# ❓ Ask your question
question = "List customers from New York"
response = agent.invoke({"input": question})

print("\n💡 Final Answer:\n", response)
