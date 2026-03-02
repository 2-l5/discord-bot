import discord
from discord.ext import commands

class QuoteBot(commands):
    def __init__(self, **options):
        super().__init__(command_prefix = "!",
                         help_command = None,
                         description = "bot that sends quotes every x hours",
                         intents = discord.Intents.all(),
                         **options)