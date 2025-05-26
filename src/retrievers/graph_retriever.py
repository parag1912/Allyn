# Graph retriever using Neo4j
from neo4j import GraphDatabase

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "test1234"

# Create Neo4j driver
driver = GraphDatabase.driver(uri, auth=(username, password))

# Define query logic
def query_graph(tx):
    cypher_query = """
    MATCH (f:Facility)-[:EXCEEDS]->(r:Regulation)
    RETURN f.name AS facility, r.type AS regulation
    """
    result = tx.run(cypher_query)
    print("\n🏭 Facilities that exceed regulations:\n")
    for row in result:
        print(f"- {row['facility']} exceeds {row['regulation']}")

# Run the session
with driver.session() as session:
    session.read_transaction(query_graph)

# Clean up
driver.close()
