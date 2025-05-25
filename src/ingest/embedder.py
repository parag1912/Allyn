# Code to embed text chunks and upload to Qdrant
import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct, CollectionStatus

# Step 1: Load parsed documents
with open("data/unstructured/parsed.jsonl", "r", encoding="utf-8") as f:
    documents = [json.loads(line) for line in f]

# Step 2: Initialize embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Step 3: Extract texts and create embeddings
texts = [doc["content"] for doc in documents]
embeddings = model.encode(texts)

# Step 4: Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)

# Step 5: Create collection (if not exists)
collection_name = "docs"
if not client.collection_exists(collection_name):
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=len(embeddings[0]), distance=Distance.COSINE)
    )

# Step 6: Upload vectors with metadata
points = [
    PointStruct(id=i, vector=embeddings[i], payload=documents[i])
    for i in range(len(embeddings))
]
client.upsert(collection_name=collection_name, points=points)

print(f"✅ Uploaded {len(points)} embeddings to Qdrant collection '{collection_name}'")
