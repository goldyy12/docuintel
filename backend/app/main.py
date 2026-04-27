from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import re
from app.core.groq import query_groq
from app.database.supabase import supabase
from app.core.loader import extract_text_from_pdf
from app.core.splitter import split_text
from app.core.vector import embed_and_store, perform_search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def clean_text(text):
    # Remove newlines and extra spaces
    cleaned = re.sub(r'\s+', ' ', text.replace('\n', ' ')).strip()
    return cleaned
@app.get("/")
def home():
    return {"message": "Hello World"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_content = await file.read()

    
    text = extract_text_from_pdf(file_content)

    chunks = split_text(text)

    status = embed_and_store(chunks,file.filename)

    return {
        "filename": file.filename,
        "total_chunks": len(chunks),
        "total_characters": len(text),
        "status": "file uploaded successfully",
        "preview": chunks[:3],
        
    }


@app.get("/search")
def search(query: str, filename: str):
    results = perform_search(query, filename)
    for r in results:
        r["content"] = clean_text(r["content"])
    results = [r for r in results if r["similarity"] > 0.25]
    results = sorted(results, key=lambda x: x["similarity"], reverse=True)[:5]
    context = "\n".join([r["content"] for r in results])
    
    answer = query_groq(query, context)
    return {
        "query": query,
        "answer": answer
    }