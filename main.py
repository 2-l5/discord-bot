import random, os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks

load_dotenv() #sets the environment variables from .env (hidden file)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

CHANNEL_ID = 1468415166075900024 
db = [] #MYSQL SOON

# SOURCE: https://gist.github.com/InterStella0/b78488fb28cadf279dfd3164b9f0cf96
class MyHelp(commands.MinimalHelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="list of commands") #creates embed object
        for cog, commands in mapping.items():
           filtered = await self.filter_commands(commands, sort=True) #filters commands that only available to users
           command_signatures = [self.get_command_signature(c) for c in filtered]
           if command_signatures: #checks if list is empty
                cog_name = getattr(cog, "qualified_name", "No Category") #prevents erroring if cog is None/No Category
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)
        embed.set_footer(text="< > is required, [ ] is optional")

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="description", value=command.help)
        embed.set_footer(text="< > is required, [ ] is optional")
        alias = command.aliases
        if alias:
            embed.add_field(name="aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)
    
    async def send_error_message(self, error):
        embed = discord.Embed(title="error", description=error) #error is a default string w/ error msg
        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = MyHelp()



""" EVENT: waits for bot to be fully initialized on discord """
@bot.event
async def on_ready():
    print(f'logged in as \"{bot.user}\"')
    if not _scheduled_message.is_running():
        _scheduled_message.start()

# SOURCE: https://pastebin.com/V3SSabxR
""" TASK: sends message, otherwise returns error and breaks loop until modified """
@tasks.loop(seconds=20)
async def _scheduled_message():
    channel = bot.get_channel(CHANNEL_ID)
    try:
        if channel:
            await channel.send(f"\"{db[random.randint(0, len(db) - 1)]}\"")
    except ValueError:
        await channel.send("no quotes available doofus")
        _scheduled_message.stop()

""" SETTER: changes the messaging frequency
    param: hours -> int
    OPTIONAL param: minutes -> int 
    OPTIONAL para: seconds -> int """
@bot.command(help="changes the messaging frequency") #decorator registers as bot command
async def schedule(ctx, hours: int = commands.parameter(description="hours")
                   , minutes: int = commands.parameter(default=0, description="minutes")
                   , seconds: int = commands.parameter(default=0, description="seconds")): 
    #ctx = context, automatic argument like self
    if _scheduled_message.is_running():
        _scheduled_message.change_interval(hours=hours, minutes=minutes, seconds=seconds)
        if hours > 0:
            await ctx.send(f"interval set to: {round(((hours * 3600) + (minutes * 60))/3600, 2)} hour(s)")
        elif minutes > 0:
            await ctx.send(f"interval set to: {minutes} minute(s)")
        else:
            await ctx.send(f"interval set to: {seconds} minute(s)")
    else:
        await ctx.send("scheduled message is not currently running")

# multiword arguments seperated by spaces are considered seperate arguments
# * is a key word only argument (idk) --> turns multiple arguments into single argument
""" SETTER: adds an item to database 
    param: quote OR link/embed OR attachment (.png, .jpg, .gif) """
@bot.command(help="adds an item to database (only text for now)", aliases=["quote"])
async def add(ctx, *, arg = commands.parameter(description="messages, images, link/embeds")):
    for i in range(len(db)):
        if arg in db[i]:
            print(f"attempted to add already existing item, {arg}, in database")
            await ctx.send("error: already exists in database")
            return 0
    db.append(arg)
    print(f"added item, {arg}, to database")
    await ctx.send("added to database")

    if not _scheduled_message.is_running():
        _scheduled_message.start()

""" SETTER: changes the channel that the bot sends messa4ge 
    param: new_channel -> int """
@bot.command(help="changes the channel that the bot sends message")
async def channel(ctx, new_channel: int = commands.parameter(description="channel id")):
    global CHANNEL_ID
    channel = bot.get_channel(new_channel)
    if channel in bot.get_all_channels():
        await channel.send("successfully changed channels!")
        CHANNEL_ID = new_channel
    else:
        await ctx.send("unsuccessfully changed channels!")



@bot.command(hidden=True)
@commands.is_owner()
async def display(ctx):
    if len(db) == 0:
        await ctx.send("no quotes available doofus")
        return 0

    string = ""
    for q in range(len(db)):
        string += db[q] + "\n"
    await ctx.send(f"{string}") #CHANGE THIS UP AFTER MYSQL

@bot.command(hidden=True, aliases=["quit"])
@commands.is_owner()
async def shutdown(ctx):
    print(f'"{bot.user}\" shutting down')
    await ctx.send("shutting down")
    await ctx.bot.close()



bot.run(os.getenv("DISCORD_TOKEN"))
