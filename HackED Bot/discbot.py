import asyncio
from asyncio import sleep
import discord
intents = discord.Intents.all()
intents.typing = False
intents.presences = False

import discord
from discord.ext import tasks, commands
import uuid
import requests
import shutil


token = (open("token.txt")).readline() #Add your own token
if(token == ""):
    print("No token found! Be sure to add your discord bot token on the first line of the token.txt file")
    input("Waiting for input to exit program...")
    quit()

client = commands.Bot(command_prefix="//",intents=intents)

@client.event

async def on_ready():
    print("Bot Live.")

@client.command()
async def save(ctx):
    try:
        url = ctx.message.attachments[0].url
    except IndexError:
        print("Error: No Attachment in the Message")
        await ctx.send("No Attachment Detected in Message") 

    else:
        if url[0:26] == "https://cdn.discordapp.com" :
            req = requests.get(url,stream = True)
            imageName = str(uuid.uuid4()) + '.jpg'
            with open(imageName,'wb') as out_file:
                print("Saving Image:" + imageName) 
                await ctx.send("Image Saved!")
                shutil.copyfileobj(req.raw, out_file)


client.run(token)

