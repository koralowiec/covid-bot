from discord.ext import commands

from bot.stats_cog import StatsCog


bot = commands.Bot(command_prefix="!covid ")


def run_bot(token: str):
    print("Bot is starting")
    bot.add_cog(StatsCog(bot))
    bot.run(token)
