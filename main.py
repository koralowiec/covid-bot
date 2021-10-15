import os

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    print("Provide Discord's Token via TOKEN environment variable!")
    exit()

bot = commands.Bot(command_prefix="!covid ")


@bot.command(name="asd")
async def asd(ctx):
    await ctx.send("Aaaaaa")


bot.run(TOKEN)
