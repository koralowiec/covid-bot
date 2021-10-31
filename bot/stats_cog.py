from discord.ext import commands

from services.records_service import RecordService


class StatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_the_latest_record = RecordService.get_the_latest_record()

    @commands.command(name="last", aliases=["ostatni", "nowy", "1"])
    async def get_the_latest_record(self, ctx):
        """Sends a message with statistics for the last recorded day.
        ---
        Zwraca statystyki dla ostatniego (zapisanego) dnia."""

        msg = RecordService.get_message_for_the_latest_record()
        await ctx.send(msg)

    @commands.command(name="avg", aliases=["średni", "śr", "sr"])
    async def get_average_for_last_7_days(self, ctx):
        """Sends a message with average statistics for the 7 days.
        ---
        Zwraca średnie statystyk z ostatniego tygodnia."""

        msg = RecordService.get_message_for_average_for_7_days()
        await ctx.send(msg)

    @commands.command(name="week", aliases=["tydzień", "7"])
    async def get_records_for_last_7_days(self, ctx):
        """Sends a message with statistics for the 7 days.
        ---
        Zwraca statystyki z ostatniego tygodnia."""

        msg = RecordService.get_message_for_7_days()
        await ctx.send(msg)

    @commands.command(name="voivodeships", aliases=["voi", "województwa", "woj"])
    async def get_the_latest_record_per_voiovdeship(self, ctx):
        """Sends a message with statistics as a table, which contains information per voivodeship.
        ---
        Zwraca tabelkę zawierającą najświeższe statystyki dla województw."""

        msg = RecordService.get_table_message_for_latest_record_per_voivodeship()
        await ctx.send(msg)
