from sentence_transformers import SentenceTransformer
from app.database.supabase import supabase

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_and_store(chunks, filename):
    embeddings = model.encode(chunks).tolist()

    data = []

    for chunk, embedding in zip(chunks, embeddings):
        data.append({
            "content": chunk,
            "embedding": embedding,
            "filename": filename  
        })

    supabase.table("documents").insert(data).execute()

    return "stored successfully"


def perform_search(query, filename):
    query_embedding = model.encode(query).tolist()

    response = supabase.rpc("match_documents", {
        "query_embedding": query_embedding,
        "match_count": 5,
        "filter": {"filename": filename}
    }).execute()

    return response.data