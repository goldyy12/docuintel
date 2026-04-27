import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.database.supabase import supabase

# Initialize Google Generative AI Embeddings
embeddings_model = None

def get_embeddings():
    global embeddings_model
    if embeddings_model is None:
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        # Updated to the latest model as per April 2026 docs
        embeddings_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-2",
            google_api_key=google_api_key
        )
    return embeddings_model

def embed_and_store(chunks, filename):
    """Embed chunks and store in Supabase"""
    model = get_embeddings()
    
    # Per docs: Prepend document structure for asymmetric retrieval
    # Format: title: {filename} | text: {chunk_content}
    formatted_chunks = [f"title: {filename} | text: {chunk}" for chunk in chunks]
    
    embeddings = model.embed_documents(formatted_chunks)

    data = [
        {
            "content": chunk, # Store original chunk for the UI
            "embedding": embedding,
            "filename": filename
        }
        for chunk, embedding in zip(chunks, embeddings)
    ]

    supabase.table("documents").insert(data).execute()
    return "stored successfully"

def perform_search(query, filename):
    """Search documents using embeddings"""
    model = get_embeddings()
    
    # Per docs: Prepend query structure for asymmetric retrieval
    # Format: task: search result | query: {query}
    formatted_query = f"task: search result | query: {query}"
    
    query_embedding = model.embed_query(formatted_query)

    response = supabase.rpc("match_documents", {
        "query_embedding": query_embedding,
        "match_count": 5,
        "filter": {"filename": filename} if filename else {}
    }).execute()

    return response.data