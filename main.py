import discord
from discord.ext import commands, tasks
from typing import Optional
from discord import app_commands
from discord.ui import Select, View
from itertools import cycle
import logging
from dotenv import load_dotenv
import asyncio
import os 

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@tasks.loop(seconds=3)
async def change_status():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(
        type=discord.ActivityType.watching, name="over tickets"))
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(
        type=discord.ActivityType.playing, name="order from us!"))
@bot.event
async def on_ready():   
    change_status.start()
    print("Bot is now online.")
    try:
        synced_commands = await bot.tree.sync()
        print("Commands synced.")
    except Exception as e:
        print("An error with syncing application commands has occured: ", e)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
