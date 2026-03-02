#todo:
# - mysql
# - create help documentation/webhook
# - update _display function
# - fix command function
# - add delete function?



import random, os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks

load_dotenv() #sets the environment variables from .env (hidden file)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

CHANNEL_ID = 1468415166075900024 
interval = 20.0
db = [] #MYSQL SOON



""" EVENT: waits for bot to be fully initialized on discord """
@bot.event
async def on_ready():
    print(f'logged in as \"{bot.user}\"')
    if not _scheduled_message.is_running():
        _scheduled_message.start()

""" GETTER: displays all commands, functionality, and parameters """
# @bot.command()
# async def help():
#     pass

""" SETTER: changes the messaging frequency
    param: hours -> float
    OPTIONAL param: minutes -> float """
@bot.command() #<-- decorator registers as bot command
async def schedule(ctx, hours: float, minutes: float = 0): #ctx = context, automatic argument like self
    global interval
    interval = hours * 360
    interval += minutes * 60
    await ctx.send(f"interval set to: {interval/360} hour(s)")

# multiword arguments seperated by spaces are considered seperate arguments
# * is a key word only argument (idk) --> turns multiple arguments into single argument
""" SETTER: adds an item to database 
    param: quote -> string OR attachment (.png, .jpg, .gif) """
@bot.command()
async def add(ctx, *, arg):
    for i in range(len(db)):
        if arg in db[i]:
            await ctx.send("error: already exists in database")
            return 0
    db.append(arg)
    await ctx.send("added to database")

    if not _scheduled_message.is_running():
        _scheduled_message.start()

""" SETTER: changes the channel that the bot sends message 
    param: new_channel -> int """
@bot.command()
async def channel(ctx, new_channel: int):
    global CHANNEL_ID
    channel = bot.get_channel(new_channel)
    try:
        if channel:
            await channel.send("successfully changed channels!")
            CHANNEL_ID = new_channel
    except AttributeError:
        await channel.send("unsuccessfully changed channels!") #PART DOESN'T RUN

""" displays everything in in database """
@bot.command()
async def _display(ctx):
    if len(db) == 0:
        await channel.send("no quotes available doofus")
        return 0

    string = ""
    for q in range(len(db)):
        string += db[q] + "\n"
    await ctx.send(f"{string}") #CHANGE THIS UP AFTER MYSQL

# Source: https://pastebin.com/V3SSabxR
""" sends message, otherwise returns error and breaks loop until modified """
@tasks.loop(seconds=interval)
async def _scheduled_message():
    channel = bot.get_channel(CHANNEL_ID)
    try:
        if channel:
            await channel.send(f"\"{db[random.randint(0, len(db) - 1)]}\"")
    except ValueError:
        await channel.send("no quotes available doofus")
        _scheduled_message.stop()



bot.run(os.getenv("DISCORD_TOKEN"))
