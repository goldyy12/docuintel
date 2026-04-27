import os

groq_client = None

def get_groq():
    global groq_client
    if groq_client is None:
        from groq import Groq
        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return groq_client


def query_groq(query, context):
    client = get_groq()

    messages = [
        {
            "role": "system",
            "content": (
                "You must ONLY use the provided context. "
                "If empty, say insert a document."
            )
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {query}"
        }
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    return response.choices[0].message.content