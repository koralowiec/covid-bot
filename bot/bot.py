from discord.ext import commands
from bot.send_info_cog import PushMessageCog

from bot.stats_cog import StatsCog


bot = commands.Bot(command_prefix="!covid ")


def run_bot(token: str):
    print("Bot is starting")
    bot.add_cog(StatsCog(bot))
    bot.add_cog(PushMessageCog(bot))
    bot.run(token)
