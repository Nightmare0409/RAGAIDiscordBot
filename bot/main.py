import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import discord
from discord.ext import commands
from dotenv import load_dotenv  # <- THIS IS REQUIRED
from rag.retriever import Retriever
from rag.generator import Generator

# Load environment variables from .env
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)




TOKEN = os.getenv("DISCORD_TOKEN")
retriever = Retriever()
generator = Generator()

# Debug print to check if token loaded
print("TOKEN loaded:", TOKEN)  # <--- Add this line

# Step 1: Define intents
intents = discord.Intents.default()
intents.message_content = True

# Step 2: Create bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Bot has connected
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Command: !ping → responds with "pong"
@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def ask(ctx, *, question):
    # Step 1: retrieve relevant docs
    docs = retriever.get_relevant_docs(question)

    # Step 2: generate response
    answer = generator.generate_answer(question, docs)

    # Step 3: send response
    await ctx.send(answer)

# Run bot
bot.run(TOKEN)