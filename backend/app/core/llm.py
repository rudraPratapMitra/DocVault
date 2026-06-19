from ollama import chat

def generate_answer(question: str,chunks:list[str]):
    context = "\n\n".join(chunks)
    prompt = f"""
    You are a document question-answering assistant.
    Use ONLY the information present in the context.
    If the answer cannot be found in the context, reply:
    "I could not find the answer in the document."
    Do not use outside knowledge.
    Context:
    {context}

    Question:
    {question}
    """
    response = chat(
        model="phi3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]