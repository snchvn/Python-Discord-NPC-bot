import discord
import asyncio
import random
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get

# Mission giver Discord bot. Randomly allocates pre-written mission scripts to members of voice channel.

# Read your Discord Bot's connecting token from token.txt [INSERT BOT TOKEN IN THIS FILE]
def read_token():
    with open("token.txt","r") as f:
        lines = f.readlines()
        return lines[0].strip()
token = read_token()
print('Token accepted')

# Read the missions.txt file with all the different missions [INSERT MISSION PARAMETERS IN THIS FILE]
def read_missions():
    with open("missions.txt","r") as f:
        lines = [i.strip() for i in f]
        return lines
missions = read_missions()
print('Mission accepted')

# Discord API calls begin here
client = discord.Client()

@client.event
async def on_message(message):
    
    channels = ["bot-test"]
   # valid_users = ["$ROLES"]
   # if str(message.channel) in channels and str(message.author) in valid_users:
    
    if str(message.channel) in channels:   
        if message.content == "!risk":
            # Shuffle missions every time !risk is called
            random.shuffle(missions)
            
            # Get list of players present in the risk voice channel
            risk_channel = client.get_channel(703786517302214737)
            members = risk_channel.members
            players = []
            for member in members:
                players.append(str(member.id))
        
            # Allocate missions to players
            for i in range(0,len(players)):
                user = discord.utils.get(client.get_all_members(), id=players[i])
                if user is not None:
                    messageContent = ("<@" + str(players[i+1]) + "> your mission is to " + missions[i])
                    await user.send(messageContent)
                    print(messageContent)
                user = discord.utils.get(client.get_all_members(), id=305136156087943179) # DIRECT USER ID IS WORKING BUT NOT players[i] VARIABLE.
                messageContent = ("<@" + str(players[0]) + "> your mission is to " + missions[0])
                print(messageContent)
                await user.send(messageContent)
                await message.channel.send("All mission orders have been issued.")

client.run(token)