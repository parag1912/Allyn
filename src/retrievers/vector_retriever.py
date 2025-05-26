from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

# Step 1: Initialize embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Step 2: Connect to local Qdrant
client = QdrantClient(host="localhost", port=6333)

# Step 3: Define query
query_text = "Who submitted the quarterly report?"
query_vector = model.encode(query_text).tolist()

# Step 4: Search top-3 similar chunks
results = client.search(
    collection_name="docs",
    query_vector=query_vector,
    limit=3
)

# Step 5: Show results
print(f"\n🔍 Top matches for: {query_text}\n")
for i, hit in enumerate(results, 1):
    print(f"{i}. 📄 Source: {hit.payload.get('source')}")
    print(f"   🧠 Content: {hit.payload.get('content')[:200]}...\n")
