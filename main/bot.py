import discord
from discord.ext import commands
import os
from os.path import join, dirname
from dotenv import load_dotenv
from main.blackjack import BlackJack


dotenv_path = join(dirname(__file__), '.env')

load_dotenv(dotenv_path)

client = commands.Bot(command_prefix=['dealer ', 'd'])


@client.event
async def on_ready():
    print('Bot is ready.')


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency)*1000}ms')


# Must be at the bottom of the script
client.add_cog(BlackJack(client))
client.run(os.getenv('_TOKEN'))
