import discord
from dotenv import load_dotenv
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='§', intents=intents)

load_dotenv()
TOKEN = os.getenv("TOKEN")
DATA_FILE = os.getenv("save_file")

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_win(user_id):
    if user_id not in data:
        data[user_id] = {"wins": 0, "points": 0}
    data[user_id]["wins"] += 1
    save_data(data)

def add_placement(user_ids):
    total_players = len(user_ids)
    for index, user_id in enumerate(user_ids):
        points = (total_players - index) * 10  # Ertser
        if user_id not in data:
            data[user_id] = {"wins": 0, "points": 0}
        data[user_id]["points"] += points
    save_data(data)


# Event Bot rdy
@bot.event
async def on_ready():
    print(f'Bot ist online als {bot.user}')

# Test von Phil
@bot.command("ping", help="PING-PONG")
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command("win", help="win a Civ Session")
@commands.has_role("CIV-ADMIN")
async def win(ctx, *ranking : discord.Member):
    for player in ranking:
        print(player.name, player.id)
    add_win(str(player.name))
    await ctx.send(f"{player.name} Du biste der Beste!!! 🏆")

# @bot.command
# async def punkte(ctx, *members: discord.Member):
#     if not members:
#         await ctx.send("Bitte gib die Platzierungen an du Dummkopf, z. B.: `!punkte @spieler1 @spieler2`")
#         return
#     add_placement([str(m.id) for m in members])
#     await ctx.send("Punkte wurden vergeben! ✅")

# @bot.command
# async def ranking(ctx):
#     if not data:
#         await ctx.send("Noo Diddy")
#         return

#     sorted_data = sorted(data.items(), key=lambda x: x[1]["points"], reverse=True)

#     msg = "**🏆 Ranking:**\n"
#     for i, (user_id, stats) in enumerate(sorted_data[:10], 1):
#         user = await bot.fetch_user(int(user_id))
#         msg += f"{i}. {user.name} – {stats['points']} Punkte / {stats['wins']} Siege\n"


print("Token:", TOKEN)
data = load_data()
bot.run(TOKEN)