import os
from openai import OpenAI

class Generator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_answer(self, question, context_docs):
        # Step 1: Prepare context
        if not context_docs:
            context = "No relevant context found."
        else:
            context = "\n\n".join(context_docs)

        # Step 2: Build prompt
        prompt = f"""
You are an AI assistant using retrieved context to answer questions.

Context:
{context}

Question:
{question}

Instructions:
- Answer clearly
- Use the context when possible
- If the answer is not in the context, say you don't know
"""

        # Step 3: Call OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        # Step 4: Return response text
        return response.choices[0].message.content