import os
from dotenv import load_dotenv 
import jellyfish
load_dotenv() 

# GET API TOKENS
discord_client_token = os.getenv('DISCORD_TOKEN')
gemini_api_key=os.getenv("GEMINI_TOKEN")

# GET ORACLE CONNECTION DETAILS
oracle_user = os.getenv("ORACLE_USER")
oracle_pass = os.getenv("ORACLE_PASS")
oracle_dsn = os.getenv("ORACLE_DSN")

# INSTANTIATE GEMINI CLIENT
from google import genai
from google.genai import types
gemini_client = genai.Client(api_key=gemini_api_key)

# INSTANTIATE DISCORD CLIENT
import discord
from discord.ext import commands
from discord import app_commands
intents = discord.Intents.default()
intents.message_content = True
#client = discord.Client(intents=intents)
#client = discord.Client(command_prefix="/",intents=intents)
bot = commands.Bot(command_prefix="/",intents = discord.Intents.all())

# DISCORD SPECIFIC VARIABLES
guild_chat_sessions = {}

# DISCORD CLIENT EVENT HANDLERS
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    #try:
    #    synced = await bot.tree.sync()
    #    print(f"Synced {len(synced)} commands")
    #except Exception as e:
    #    print(e)

@bot.tree.command(name="sync",description="syncs any new slash commands")
async def sync(interaction: discord.Interaction):
    await bot.tree.sync()
    await interaction.response.send_message("commands synced")

@bot.tree.command(name="zawarldo",description="You're next words are:")
async def lockIn(interaction: discord.Interaction, phrase: str, user:str):
    #guild = discord.Interaction.
    await interaction.response.send_message(phrase,ephemeral=True)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mention in message.content:
        # Create a new chat session for the guild if it doesn't exist
        if message.guild.id not in guild_chat_sessions:
            guild_chat_sessions[message.guild.id] = gemini_client.chats.create(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                system_instruction="You are Dr. Doofenshmirtz from the show Phineas and Ferb. You are a mad scientist who is trying to take over the world. You are very smart and have a lot of knowledge about science and technology. You are also very funny and have a great sense of humor. You like to make jokes and puns, but you can also be serious when you need to be. You are always looking for new inventions and ways to improve your evil plans.",
                max_output_tokens=250,
                temperature=0.7)
            )

        # Fetch the current guild's chat session and the received message
        chat = guild_chat_sessions[message.guild.id]    
        response = chat.send_message(message.content)

        await message.channel.send(response.text)

bot.run(token=discord_client_token)