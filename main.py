import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)

for i in os.listdir("./verify"):
    if i.endswith(".py"):
        bot.load_extension(f"verify.{i[:-3]}")

@bot.event
async def on_ready():
    print("▬"*30 + f"\n{bot.user.name} is ready..\n" + "▬"*30)


bot.run("YOUR TOKEN")