import asyncio, random, os
from dotenv import load_dotenv

import discord
from discord.ext import commands, tasks

load_dotenv() #sets the environment variables from .env

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

quotes = [] #so i need an external database because this script will not run forever and data will be lost

@bot.command() #<-- decorator registers as bot command
async def set_interval(ctx, hours: int, minutes: int = None): #ctx = context, automatic argument
    global interval
    interval += hours * 360

    if minutes != None:
        interval += minutes * 60

# multiword arguments seperated by spaces are considered seperate arguments
# * is a key word only argument (idk) --> turns multiple arguments into single argument
@bot.command()
async def add_quote(ctx, *, arg):
    for i in range(len(quotes)):
        if arg in quotes[i]:
            await ctx.send("quotes already in there")
            return 0

    quotes.append(arg)
    await ctx.send("ok, i added it")

# @bot.command()
# async def add_attachment(ctx, *, arg):
#     pass #check if already existing

#DEBUGGING COMMANDS
@bot.command()
async def test(ctx):
    await ctx.send("hi")

@bot.command()
async def send_quote(ctx):
    try:
        await ctx.send(quotes[random.randint(0, (len(quotes) - 1))]) #i need to fix this
    except ValueError:
        await ctx.send("no quotes available doofus")

@bot.command()
async def display_all_quotes(ctx):
    await ctx.send(quotes)

#RUN-TIME
# def main():
#     pass

bot.run(os.getenv("DISCORD_TOKEN"))