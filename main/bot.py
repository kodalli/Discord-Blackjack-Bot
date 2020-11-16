import discord
from discord.ext import commands
import asyncio
import os

client = commands.Bot(command_prefix=['dealer'])


# Event detects if a specific activity has happened
@client.event
async def on_ready():
    print('Bot is ready.')


@client.command()
async def play(ctx):
    # await ctx.send()
    pass


@client.command()
async def hit(ctx):
    pass


@client.command()
async def stand(ctx):
    pass
