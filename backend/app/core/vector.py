import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.database.supabase import supabase

# Initialize Google Embeddings (Uses API instead of local RAM)
embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def embed_and_store(chunks, filename):
    # This sends the chunks to Google Cloud and gets back the vectors
    embeddings = embeddings_model.embed_documents(chunks)

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
    # This sends your search query to Google Cloud
    query_embedding = embeddings_model.embed_query(query)

    response = supabase.rpc("match_documents", {
        "query_embedding": query_embedding,
        "match_count": 5,
        "filter": {"filename": filename}
    }).execute()

    return response.data