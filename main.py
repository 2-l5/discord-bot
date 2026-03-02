#todo:
# - SQLite on raspberry pi
# - update _display function
# - fix command function
# - add delete function?

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from bot import QuoteBot

if __name__ == "__main__":
    bot = QuoteBot()
    load_dotenv() #sets the environment variables from .env (hidden file)
    bot.run(os.getenv("DISCORD_TOKEN"))
