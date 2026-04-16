#Import system-level functions (used for modifying Python's import paths)
import sys

#Import OS utilities (used for file paths and environment variables)
import os


#Add the parent directory to Python's path so we can import modules from outside this folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#Import the main Discord library
import discord

#Import command handling tools from Discord
from discord.ext import commands

#Import function to load environment variables from a .env file (keeps secrets safe)
from dotenv import load_dotenv  # <- THIS IS REQUIRED

#Import custom Retriever (finds relevant documents)
from rag.retriever import Retriever

#Import custom Generator (creates AI responses)
from rag.generator import Generator


#Import Path for easier and safer file path handling
from pathlib import Path


#Build the path to the .env file (go up two folders, then find ".env")
env_path = Path(__file__).resolve().parent.parent / ".env"

#Load environment variables from the .env file
load_dotenv(dotenv_path=env_path)




#Get the Discord bot token from environment variables
TOKEN = os.getenv("DISCORD_TOKEN")

#Create an instance of the Retriever (used for searching knowledge)
retriever = Retriever()

#Create an instance of the Generator (used for generating answers)
generator = Generator()


#Print the token to confirm it loaded correctly (for debugging)
print("TOKEN loaded:", TOKEN)  # <--- Add this line


#Create default Discord bot permissions (intents)
intents = discord.Intents.default()

#Enable access to message content (required for reading user messages)
intents.message_content = True


#Create the bot with a command prefix "!" (e.g., !ask, !ping)
bot = commands.Bot(command_prefix="!", intents=intents)


#Store recent conversation history (used for context in AI responses)
chat_history = []


#Define a command "!clear" to reset conversation memory
@bot.command()
async def clear(ctx):

    #Use global variable so we can modify chat_history
    global chat_history

    #Reset chat history to an empty list
    chat_history = []

    #Send confirmation message in Discord
    await ctx.send("🧹 Conversation memory cleared.")


#Event that runs when the bot successfully connects to Discord
@bot.event
async def on_ready():

    # Print confirmation in the terminal
    print(f'{bot.user} has connected to Discord!')


#Define a simple "!ping" command to test if the bot is working
@bot.command()
async def ping(ctx):

    #Respond with "pong"
    await ctx.send("pong")


#Define the main AI command "!ask"
@bot.command()
async def ask(ctx, *, question):

    #Retrieve relevant documents based on the user's question
    docs = retriever.retrieve(question)

    #Generate an answer using the question, retrieved docs, and chat history
    answer = generator.generate_answer(
        question,
        docs,
        chat_history
    )

    #Save the question and answer to conversation history
    chat_history.append((question, answer))

    #Keep only the last 5 interactions to limit memory size
    if len(chat_history) > 5:
        chat_history.pop(0)

    #Send the generated answer back to Discord
    await ctx.send(answer)


#Event that runs whenever any message is sent in the server
@bot.event
async def on_message(message):

    #Ignore messages sent by the bot itself (prevents infinite loops)
    if message.author == bot.user:
        return

    #Open the memory file in append mode to store messages
    with open("data/knowledge_base/discord_memory.txt", "a", encoding="utf-8") as f:

        # Write the message content to the file
        f.write(message.content + "\n")

    #Allow commands (like !ask) to still function
    await bot.process_commands(message)


#Start the bot using the token
bot.run(TOKEN)