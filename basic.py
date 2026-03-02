import discord
from discord.ext import commands
import event
import bot

class Basic(commands.Cog):
    def __init__(self, interval):
        pass

        self.CHANNEL_ID = 1468415166075900024 
        self.interval = interval
        self.db = [] #MYSQL SOON

    """ changes the messaging frequency
        param (float):  hours
        param (optional, float):  minutes"""
    @commands.command() #<-- decorator registers as bot command
    async def schedule(self, ctx, hours: float, minutes: float = 0): #ctx = context, automatic argument like self
        self.interval = hours * 360
        self.interval += minutes * 60
        await ctx.send(f"interval set to: {round(self.interval/360)} hour(s)")

    # multiword arguments seperated by spaces are considered seperate arguments, * is a key word only argument (idk) --> turns multiple arguments into single argument
    """ adds an item to database 
        param (string): quote"""
    @commands.command()
    async def add(self, ctx, *, arg):
        for i in range(len(db)):
            if arg in db[i]: #CHANGE THIS AFTER SQLite
                await ctx.send("error: already exists in database")
                return 0
        db.append(arg)
        await ctx.send("added to database")

        if not event._scheduled_message.is_running():
            event._scheduled_message.start()

    """ deletes an existing item from database
        param (string): existing quote in database"""
    # @bot.command()
    # async def delete(ctx, quote: str): #CHANGE THIS AFTER SQLite
    #     pass

    """ changes the channel that the bot sends message 
        param (int): new_channel """
    @commands.command(aliases=["change channel"])
    async def channel(self, ctx, new_channel: int):
        channel = bot.get_channel(new_channel)
        try:
            if channel:
                await channel.send("successfully changed channels!")
                self.CHANNEL_ID = new_channel
        except AttributeError:
            await channel.send("unsuccessfully changed channels!") #PART DOESN'T RUN


#debugging commands
    async def get_channel(self):
        return self.CHANNEL_ID

    async def get_interval(self, ctx):
        return self.interval

    async def display(self, ctx):
        if len(db) == 0:
            await ctx.send("no quotes available doofus") #idk
            return 0

        string = ""
        for q in range(len(db)):
            string += db[q] + "\n"
        await ctx.send(f"{string}") #CHANGE THIS AFTER SQLite