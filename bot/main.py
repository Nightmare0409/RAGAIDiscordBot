import os
import discord
from discord.ext import commands
from dotenv import load_dotenv  # <- THIS IS REQUIRED


# Load environment variables from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

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

# Run bot
bot.run(TOKEN)