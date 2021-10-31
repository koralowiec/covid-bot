from discord.ext import commands
from bot.send_info_cog import PushMessageCog

from bot.stats_cog import StatsCog

default_prefix = "!covid"


def run_bot(token: str, prefix: str = default_prefix):
    # Appending a space after the prefix
    prefix = f"{prefix} "
    bot = commands.Bot(command_prefix=prefix)
    print(f"Bot will be available with prefix: {prefix}")
    print("Bot is starting")
    bot.add_cog(StatsCog(bot))
    bot.add_cog(PushMessageCog(bot))
    bot.run(token)
