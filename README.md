# 📚 AI Document Intelligence (RAG System)

A full-stack AI-powered document question-answering system built using Retrieval-Augmented Generation (RAG).
Upload PDFs and ask questions — the system retrieves relevant context and generates accurate answers using LLMs.

## 🚀 Features
- 📄 Upload PDF documents
- ✂️ Automatic text extraction & chunking
- 🧠 Semantic search using embeddings
- ⚡ Fast LLM responses using Groq
- 🗂️ Vector storage with Supabase (pgvector)
- 🔍 Context-aware question answering
- 🌐 CORS-enabled API for frontend integration

## 🏗️ Tech Stack

**Backend**
- FastAPI
- Python

**AI / ML**
- SentenceTransformers (embeddings)
- Groq (LLM inference)

**Database**
- Supabase (PostgreSQL + pgvector for vector search)

## ⚙️ How It Works

1. **Upload PDF**
   - Extract text from file
   - Split into chunks

2. **Embedding**
   - Convert chunks into vector embeddings using SentenceTransformers
   - Store in Supabase (pgvector)

3. **Search**
   - User query → embedding
   - Perform similarity search

4. **Generation**
   - Retrieve top matching chunks
   - Send context to LLM (Groq)
   - Return final answer

## 📡 API Endpoints

### `GET /`
Health check

\`\`\`json
{
  "message": "Hello World",
  "status": "ok"
}
\`\`\`
