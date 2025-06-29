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
    SERVER_ID = os.getenv("SERVER_ID")
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

    # Change elos after an Win
    @bot.tree.command(name="win", description="Player Ranking of the Game")
    @app_commands.describe(
        player1="First Player",
        player2="Second Player",
        player3="Third Player",
        player4="Fourth Player",
        player5="Fifth Player",
        player6="Sixth Player",
        player7="Senventh Player",
        player8="Eighth Player",
        )
    async def win(interaction:discord.Interaction, player1: discord.Member, player2: discord.Member, player3: discord.Member = None, player4: discord.Member = None, player5: discord.Member = None, player6: discord.Member = None, player7: discord.Member = None, player8: discord.Member = None):
        ranking = [player for player in [player1, player2, player3, player4, player5, player6, player7, player8] if player is not None]
        dm.update_elo([str(player.name) for player in ranking])
        data = dm.load_data()
        msg_text = ""
        for rank, player in enumerate(ranking):
            print(player.display_name, player.id)
            if rank == 0:
                msg_text += f"{player.mention} Du biste der Beste!!! 🎖️ elo: {data[player.name]["elo"]}     |     {data[player.name]["wins"]} / {data[player.name]["games"]} wins!\n"
            else:
                
                msg_text += f"{player.mention} der {rank+1}. elo: {data[player.name]["elo"]}     |     {data[player.name]["wins"]} / {data[player.name]["games"]} wins!\n"
        await interaction.response.send_message(msg_text)

    @bot.tree.command(name="ranking", description="Current Ranking of all Players")
    async def ranking(interaction:discord.Interaction):
        data = dm.load_data()
        ranked = sorted(data, key=lambda user_id: data[user_id]["elo"], reverse=True)

        msg = "**Hoheitliches Führerbrett🏆**\n"

        for place, user_id in enumerate(ranked, start=1):
            msg += f"{place}. {interaction.guild.get_member_named(user_id).mention}, {data[user_id]["elo"]} \n"
            
        await interaction.response.send_message(msg)
    
    @bot.tree.command(name="set-ranking", description="change a Players elo to a custom value")
    @app_commands.describe(player="Choosen Player", new_elo="new Elo")
    async def set_ranking(interaction:discord.Interaction, player: discord.Member, new_elo: int):
        print(type(new_elo))
        data = dm.load_data()
        data[player.name]["elo"] = new_elo
        dm.save_data(data)

        await interaction.response.send_message(f"Elo changed, new elo: {new_elo}")
    
    return bot


