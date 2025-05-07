import os
import asyncio
import jellyfish
from dotenv import load_dotenv 
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
async def lockIn(interaction: discord.Interaction, phrase: str, user:discord.Member):
    await interaction.response.send_message(f"Prediction locked in! Waiting for {user.mention}'s next 3 messages...", ephemeral=True)

    for i in range(3):
        try:
            message = await bot.wait_for(
                "message", 
                check=lambda message: message.channel == interaction.channel and message.author == user, 
                timeout=60
            )
            similarity_value = jellyfish.jaro_similarity(phrase, message.content)
            if similarity_value > 0.8:
                embed = discord.Embed(colour=0x00b0f4)
                embed.description = f"You've been Zawarldo'd! {interaction.user.mention} predicted your next message in 4K"
                embed.add_field(name=f"{interaction.user.display_name}'s Message:",
                                value= phrase,
                                inline=False)
                embed.add_field(name=f"{user.display_name}'s Message:",
                                value=message.content,
                                inline=False)
                embed.set_image(url="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbjhrMG9vOGUweGk5MXpjY3YzcWV3cTNjem45Z3E0dnlmcWc2Nmd5OCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/uISzZpAzbQ4nK/giphy.gif")
                await interaction.channel.send(embed=embed)
                return          
        except asyncio.TimeoutError:
            return

    embed = discord.Embed(colour=0x00b0f4)
    embed.description = f"{interaction.user.display_name} tried to predict your message and was wrong. -Aura"
    embed.add_field(name=f"{interaction.user.display_name} thought you would say:",
                value= phrase,
                inline=False)
    embed.set_image(url="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDA3MmZtcWsybHJ3eGt3YW9lcjNlM3Z0Ynk1dnkyb2VjbDhwNWpjNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/pNn4hlkovWAHfpLRRD/giphy.gif")

    await interaction.channel.send(embed=embed)

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