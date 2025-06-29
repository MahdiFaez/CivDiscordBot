import discord
from dotenv import load_dotenv
from discord.ext import commands
import civ_bot
import json
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
DATA_FILE = os.getenv("save_file")

civ_bot = civ_bot.initialize_bot()

print("Token:", TOKEN)
civ_bot.run(TOKEN)