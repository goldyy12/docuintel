import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.database.supabase import supabase


embeddings_model = None

def get_embeddings():
    global embeddings_model
    if embeddings_model is None:
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
       
        embeddings_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-2",
            google_api_key=google_api_key
        )
    return embeddings_model

def embed_and_store(chunks, filename):
    
    model = get_embeddings()
    
  
    formatted_chunks = [f"title: {filename} | text: {chunk}" for chunk in chunks]
    
    embeddings = model.embed_documents(formatted_chunks)

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
    
    
    formatted_query = f"task: search result | query: {query}"
    
    query_embedding = model.embed_query(formatted_query)

    response = supabase.rpc("match_documents", {
        "query_embedding": query_embedding,
        "match_count": 5,
        "filter": {"filename": filename} if filename else {}
    }).execute()

    return response.data