# Import the built-in os module to access environment variables
import os
# Import the OpenAI client for making API calls
from openai import OpenAI

# Define a class responsible for generating answers
class Generator:
    # Initialize the Generator
    def __init__(self):
        # Create an OpenAI client using the API key from environment variables
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Define a method to generate an answer from a question and context
    def generate_answer(self, question, context_docs, chat_history=None):
        # Combine all context documents into one string separated by blank lines
        context = "\n\n".join(context_docs) if context_docs else "No relevant context found."

        # Initialize an empty string to store formatted chat history
        history_text = ""
        # Check if there is any previous chat history
        if chat_history:
            # Loop through each question-answer pair in the history
            for q, a in chat_history:
                # Format and append each interaction to the history string
                history_text += f"User: {q}\nAssistant: {a}\n"

        # Create a prompt string that includes history, context, and the question
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

        # Send a request to the OpenAI API to generate a response
        response = self.client.chat.completions.create(
            # Specify the model to use for generating responses
            model="gpt-4o-mini",
            # Provide system and user messages to guide the model
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            # Control randomness (lower = more deterministic output)
            temperature=0.3
        )

        # Return the generated text from the response
        return response.choices[0].message.content