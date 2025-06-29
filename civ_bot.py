# TODO: Formel Rank: Pionts = ((players+1)-place)*5
import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from utils.dataManagment import DataManager
import json
import os


def initialize_bot():
    DATA_FILE = os.getenv("save_file")
    dm = DataManager(DATA_FILE)

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix='§', intents=intents)
    
    # Event Bot rdy
    @bot.event
    async def on_ready():
        print(f'Bot ist online als {bot.user}')
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)



    # Check connection to Server
    @bot.command("ping", help="PING-PONG")
    async def ping(ctx):
        await ctx.send('Pong!')

    # Update elo after a win
    @bot.tree.command(name="win")
    @commands.has_role("CIV-ADMIN")
    async def win(ctx, *ranking : discord.Member):
        dm.update_elo([str(player.name) for player in ranking])
        data = dm.load_data()
        msg_text = ""
        for rank, player in enumerate(ranking):
            print(player.display_name, player.id)
            if rank == 0:
                msg_text += f"{player.mention} Du biste der Beste!!! 🎖️ elo: {data[player.name]["elo"]}     |     {data[player.name]["wins"]} / {data[player.name]["games"]} wins!\n"
            else:
                
                msg_text += f"{player.mention} der {rank+1}. elo: {data[player.name]["elo"]}     |     {data[player.name]["wins"]} / {data[player.name]["games"]} wins!\n"
        await ctx.send(msg_text)
    
    @bot.tree.command("ranking")
    async def ranking(ctx):
        data = dm.load_data()
        ranked = sorted(data, key=lambda user_id: data[user_id]["elo"], reverse=True)

        msg = "**Hoheitliches Führerbrett🏆**\n"

        for place, user_id in enumerate(ranked, start=1):
            msg += f"{place}. {ctx.guild.get_member_named(user_id).mention}, {data[user_id]["elo"]} \n"
            
        await ctx.send(msg)

    
    @bot.tree.command("set-ranking")
    async def set_ranking(ctx, player: discord.Member, new_elo: int):
        print(type(new_elo))
        data = dm.load_data()
        data[player.name]["elo"] = new_elo
        dm.save_data(data)

        await ctx.send(f"Elo changed, new elo: {new_elo}")


    return bot


