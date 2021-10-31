from discord.ext import commands

from services.records_service import RecordService


class StatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_the_latest_record = RecordService.get_the_latest_record()

    @commands.command(name="last")
    async def get_the_latest_record(self, ctx):
        """Sends a message with statistics for the last recorded day"""

        msg = RecordService.get_message_for_the_latest_record()
        await ctx.send(msg)

    @commands.command(name="avg")
    async def get_average_for_last_7_days(self, ctx):
        """Sends a message with average statistics for the 7 days"""

        msg = RecordService.get_message_for_average_for_7_days()
        await ctx.send(msg)

    @commands.command(name="week")
    async def get_records_for_last_7_days(self, ctx):
        """Sends a message with statistics for the 7 days"""

        msg = RecordService.get_message_for_7_days()
        await ctx.send(msg)
