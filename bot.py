import discord
import random
import os


# Mission giver Discord bot. Randomly allocates pre-written mission scripts to members of voice channel.

# Read your Discord Bot's connecting token from Heroku config vars
access_token = os.environ["ACCESS_TOKEN"]
channel_id = os.environ["CHANNEL_ID"]

# Read the missions.txt file with all the different missions [INSERT MISSION PARAMETERS IN THIS FILE]
def read_missions():
    with open("missions.txt","r") as f:
        lines = [i.strip() for i in f]
        return lines

missions = read_missions()

# Discord API calls begin here
client = discord.Client()
@client.event
async def on_message(message):
    
   # Use below code to define mission invocation by user role
   # valid_users = ["$ROLES"]
   # if str(message.channel) in channels and str(message.author) in valid_users:
    channels = ["bot-commands"]
    if str(message.channel) in channels:   
        
        # Setting the !risk command
        if message.content == "!risk":
            
            # Shuffle missions every time !risk is called
            random.shuffle(missions)
            
            # Get list of players present in the risk voice channel [Replace this with your own channel ID]
            risk_channel = client.get_channel(int(channel_id))
            members = risk_channel.members
            
            # Generate a list of player IDs
            players = []
            for member in members:
                players.append(str(member.id))

            # Exit clause when script is invoked with no players
            if len(players)==0:
                await message.channel.send("Mission abort. There are no players on the Risk voice channel.")
            
            else:
                # Allocate missions to players
                for i in range(0,len(players)):
                    
                    # Get the user element from the iterable player ID (GOT STUCK HERE FOR 2 HOURS PASSING INTEGER AS STRING)
                    player = discord.utils.get(client.get_all_members(), id=int(players[i]))
                    
                    # Compose message for each player allocating their respective mission
                    messageContent = ("<@" + str(players[i]) + "> your mission is to " + missions[i])
                    #Send a DM to each player
                    await player.send(messageContent)

                await message.channel.send("Mission orders issued successfully.")

client.run(access_token)