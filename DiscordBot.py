import discord
from discord import Intents, Client, Message
from discord.ext import commands
import random
import asyncio
import pickle
import os
import shutil
import webbrowser
import requests
import re


command_prefix = ';'
intents: Intents = Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=command_prefix, intents = intents)

# Name of Servers the bot is in
@client.command()
async def servers(ctx):
    async for guild in client.fetch_guilds(limit=150):
        print(guild.name)
    await ctx.send('Servers sent to Terminal')

# Cooldown for specific commands
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send(f"Please wait {round(error.retry_after, 2)} seconds!")

# Download Emotes command
@client.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def emotes_download(ctx):
    loading = await ctx.send('Downloading Emotes...')
    # Check if folder exists. If not, create it.
    if not os.path.exists(ctx.guild.name + " Emotes"):
        os.makedirs(ctx.guild.name + " Emotes")
    # Download all emotes from server where command called.
    for line in ctx.guild.emojis:
        #line.url = "https://cdn.discordapp.com/emojis/" + str(line.id) + ".png?v=1"
        response = requests.get(line.url)
        if line.url.endswith(".gif"):
            path = ctx.guild.name + " Emotes" + "/" + line.name + ".gif"
        else:
            path = ctx.guild.name + " Emotes" + "/" + line.name + ".png"
        with open(path, "wb") as file:
            file.write(response.content)
    # Zips, uploads to discord, then deletes zip and folder.
    shutil.make_archive(ctx.guild.name + " Emotes", 'zip', ctx.guild.name + " Emotes")
    await loading.delete()
    await ctx.send(file=discord.File(ctx.guild.name + " Emotes.zip"))
    shutil.rmtree(ctx.guild.name + " Emotes")
    os.remove(ctx.guild.name + " Emotes.zip")


# Dice Roll Command 1-100
@client.command()
async def roll(ctx):
    # random.randrange(min,max) This is a roll function.
    message = random.randrange(1, 100)
    await ctx.send(message)


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


# Clear Command, checks for permissions
@client.command()
async def clear(ctx, amount=5):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.send('No permissions!')

@client.command()
async def join(ctx):
    await client.connect(timeout=60.0,reconnect=True)

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb, activity= discord.Game("OwO"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('Discord Version:', discord.__version__)
    print('------')

with open('token.txt', 'r') as file:
    token = file.read().replace('\n', '')
client.run(token)