from discord import File
from discord.ext import commands
from services.chart_service import ChartService

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

    @commands.command(name="chart", aliases=["wykres"])
    async def get_charts(self, ctx, chart_type: int, *args):
        """Show a chart.
        Types of chart:
        1 - daily (`!covid chart 1 number_of_days`)
        2 - daily for a voivodeship (`!covid chart 2 voivodeship_name`)
        3 - total (`!covid chart 3 number_of_days`)
        ---
        pl"""

        if chart_type == 1:
            number_of_days = 7

            if len(args) > 0:
                number_of_days = int(args[0])

            ChartService.plot_n_latest_records(config="daily", n=number_of_days)
        elif chart_type == 2:
            voivodeship = args[0]

            ChartService.plot_n_latest_records(
                config="daily", n=7, voivodeship_name=voivodeship
            )
        elif chart_type == 3:
            number_of_days = 30

            if len(args) > 0:
                number_of_days = int(args[0])

            ChartService.plot_n_latest_records(
                config="total", n=number_of_days, chart=True
            )
        else:
            await ctx.send("Not valid type of chart.\nNiepoprawny typ wykresu.")
            return

        with open("plot.png", "rb") as file_chart:
            file = File(file_chart, filename="plot.png")

        await ctx.send(file=file)
