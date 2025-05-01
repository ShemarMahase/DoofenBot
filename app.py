import os
from dotenv import load_dotenv 
load_dotenv() 

# GET API SECRETS FROM ENVIRONMENT VARIABLES
discord_client_token = os.getenv('DISCORD_TOKEN')
gemini_api_key=os.getenv("GEMINI_TOKEN")

# INSTANTIATE GEMINI CLIENT
from google import genai
from google.genai import types
gemini_client = genai.Client(api_key=gemini_api_key)

# INSTANTIATE DISCORD CLIENT
import discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# DISCORD SPECIFIC VARIABLES
guild_chat_sessions = {}

# DISCORD CLIENT EVENT HANDLERS
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mention in message.content:
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

client.run(token=discord_client_token)