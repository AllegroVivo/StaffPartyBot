from __future__ import annotations

import os

from discord import Intents
from dotenv import load_dotenv

from Classes.Bot import TrainingBot
################################################################################

load_dotenv()

################################################################################

if os.getenv("DEBUG") == "True":
    debug_guilds = [303742308874977280, 955933227372122173]
else:
    debug_guilds = None
    
bot = TrainingBot(
    description="Toot toot, bitches!",
    intents=Intents.all(),
    debug_guilds=debug_guilds
)

################################################################################

for filename in os.listdir("Cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"Cogs.{filename[:-3]}")

################################################################################

if os.getenv("DEBUG") == "True":
    token = os.getenv("DEBUG_TOKEN")
else:
    token = os.getenv("DISCORD_TOKEN")
    
bot.run(token)

################################################################################
