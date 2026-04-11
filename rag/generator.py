import os
from openai import OpenAI

class Generator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_answer(self, question, context_docs, chat_history=None):
        context = "\n\n".join(context_docs) if context_docs else "No relevant context found."

        history_text = ""
        if chat_history:
            for q, a in chat_history:
                history_text += f"User: {q}\nAssistant: {a}\n"

        prompt = f"""
You are an AI assistant using retrieved context and conversation history.

Conversation History:
{history_text}

Context:
{context}

Question:
{question}

Answer clearly and accurately.
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content