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
import pickle
import os

#Custom Imports:
import img2txt

token = (open("token.txt")).readline() #Add your own token
if(token == ""):
    print("No token found! Be sure to add your discord bot token on the first line of the token.txt file")
    input("Waiting for input to exit program...")
    quit()

client = commands.Bot(command_prefix=".",intents=intents)

def load():
    #open python pickle file within the same directory, if it doesnt exist, ensure it exists
    try:
        with open("usernames.pickle", "rb") as f:
            usernames = pickle.load(f)
    except FileNotFoundError:
        with open("usernames.pickle", "wb") as f:
            usernames = {}
            pickle.dump(usernames, f)
    return usernames

@client.event

async def on_ready():
    print("Bot Live.")

@client.command()
async def save(ctx):
    userid = str(ctx.author.id)
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
    cwd = os.getcwd()
    #create path with os.path.join(
    path = os.path.join(cwd, "imageName")
    temp = img2txt.process(path)
    usernames = load()
    if not userid in usernames:
        await ctx.send("You have not registered your username yet!")
    else:
        if usernames[userid][0] in temp:
            kd = temp[usernames[userid][0]]
            usernames[userid][1].append(kd)
        else:
            await ctx.send("Your username is not in this screenshot!")
    #await saveusername(ctx, name)

    
    #print("Name of player is" , name)
    #print("Kills:" , kd[0], "\nDeaths:", kd[1])



@client.command()
async def saveusername(ctx, query=""):
    userid = str(ctx.author.id)
    #associate discord id with username
    if query == "":
        await ctx.send("Please enter a username")
    else:
        #open python pickle file within the same directory, if it doesnt exist, ensure it exists
        usernames = load()
        #check if discord userid exists in dictionary, if not, add key
        if str(ctx.author.id) not in usernames:
            usernames[userid] = [query,[]]  #FORMAT: DiscordID: [Game Username, KDA History]
            #kda history = [[kills,deaths], [kills,deaths], [kills,deaths]]
            await ctx.send("Username saved!")
            print(usernames[ctx.author.id])
       
        #save the dictionary with pickle
        with open("usernames.pickle", "wb") as f:
            pickle.dump(usernames, f)


@client.command()
async def updateusername(ctx, query=""):    
    #updates the user's name in the dict
    userid = str(ctx.author.id)
    if query == "":
        await ctx.send("Please enter a username")
    else:
        #open python pickle file within the same directory, if it doesnt exist, ensure it exists
        usernames = load()
        #check if discord userid exists in dictionary, if not, add key
        if userid not in usernames:
            await ctx.send("Nothing to update")
        else:
            usernames[userid][0] = query
            await ctx.send("Username updated!")
            print(usernames[userid][0])
       
        #save the dictionary with pickle
        with open("usernames.pickle", "wb") as f:
            pickle.dump(usernames, f)

async def showleaderboard(ctx, query=""): 
    #new function that calculates the score and spits it out as a leaderboard in an embed using the image parser amogh and andrew made
    userid = str(ctx.author.id)
    usernames = load()
    if not userid in usernames:
        await ctx.send("You have not registered your username yet!")
    else:
        averages = {}
        for user in usernames:
            if len(usernames[user][1]) > 0:
                #averages[user] = (sum(usernames[user][1][0])/len(usernames[user][1][1]))
                #averages[user]
                kills = 0
                deaths = 0
                for i in range(len(usernames[user][1])): #iterate through history
                    kills+= (usernames[user][1][i][0])
                    deaths+= (usernames[user][1][i][0])
                averages[user] = kills/deaths
            else:
                averages[user] = usernames[user][1][0][0]/usernames[user][1][0][1]
            #generate top 10 leaderboard from greatest values in averages
            leaderboard = sorted(averages.items(), key=lambda x: x[1], reverse=True)
            leaderboard = leaderboard[:10]
            #generate embed
            embed = discord.Embed(title="Leaderboard", description="Top 10 Players", color=0xeee657)
            for i in range(len(leaderboard)):
                embed.add_field(name="Player - KDA", value=str(leaderboard[i][0]+" - "+leaderboard[i][1]), inline=True)

        print(averages)

        embed = discord.Embed(title="Leaderboard:",description=f"",colour=ctx.author.colour)
        msg = await ctx.send(embed=embed)
        

client.run(token)

