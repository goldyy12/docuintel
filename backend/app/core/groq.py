from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


def query_groq(query, context):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that answers questions "
                "You must ONLY use the provided context. "
                 "If the database is empty , say insert a document to get started."
                "If the answer is not in the context, say you don't know."
               
            )
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {query}"
        }
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.5
    )

    return response.choices[0].message.content