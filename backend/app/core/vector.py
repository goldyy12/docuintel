import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.database.supabase import supabase

# Initialize Google Embeddings (Uses API instead of local RAM)
import os
from app.database.supabase import supabase

embeddings_model = None

def get_embeddings():
    global embeddings_model
    if embeddings_model is None:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        embeddings_model = GoogleGenerativeAIEmbeddings(
            model="models/embedding-004",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
    return embeddings_model
def embed_and_store(chunks, filename):
    model = get_embeddings()

    embeddings = model.embed_documents(chunks)

    data = [
        {
            "content": chunk,
            "embedding": embedding,
            "filename": filename
        }
        for chunk, embedding in zip(chunks, embeddings)
    ]

    supabase.table("documents").insert(data).execute()

    return "stored successfully"
def perform_search(query, filename):
    model = get_embeddings()

    query_embedding = model.embed_query(query)

    response = supabase.rpc("match_documents", {
        "query_embedding": query_embedding,
        "match_count": 5,
        "filter": {"filename": filename}
    }).execute()

    return response.data