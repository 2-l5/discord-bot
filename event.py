import discord
import random
from discord.ext import commands, tasks
from discord.ext.commands import errors
from discord.ext.commands import command
import bot, basic

class Event(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'logged in as \"{bot.user}\"')
        if not self._scheduled_message.is_running():
            self._scheduled_message.start()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("missing required arguments", delete_after=5)
        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.send(f"command not found :sob:\ntype !help for more info", delete_after=5) #prefix
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send("invalid argument", delete_after=5)
        else:
            raise error
    
    # Source: https://pastebin.com/V3SSabxR
    """ sends message, otherwise returns error and breaks loop until modified """
    @tasks.loop(seconds=basic._get_interval())
    async def _scheduled_message(self):
        channel = bot.get_channel(CHANNEL_ID)
        try:
            if channel:
                await channel.send(f"\"{db[random.randint(0, len(db) - 1)]}\"")
        except ValueError:
            await channel.send("no quotes available doofus")
            self._scheduled_message.stop()

def setup(bot):
    bot.add_cog(Event(bot))