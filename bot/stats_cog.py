from typing import Tuple
from discord.ext import commands

from db.records_service import RecordService


class StatsCog(commands.Cog):
    record_message_template = """
Dane z {date}
Liczba nowych zakażeń: {daily_infected}
Liczba nowych zgonów: {daily_dead}
Liczba nowych ozdrowień: {daily_recovered}
"""

    average_message_tempalte = """
Średnia z {number_of_days} dni:
Zakażeń dziennie: {avg_daily_infected}
Zgonów dziennie: {avg_daily_dead}
Ozdrowień dziennie: {avg_daily_recovered}
"""

    def __init__(self, bot):
        self.bot = bot

    @classmethod
    def get_message_for_record(cls, record):
        return cls.record_message_template.format(
            date=record.date,
            daily_infected=record.daily.infected,
            daily_dead=record.daily.dead,
            daily_recovered=record.daily.recovered,
        )

    @staticmethod
    def get_average_of(attribute: str, records) -> Tuple[int, int]:
        num_of_records = len(records)
        return (
            int(sum(r.daily[attribute] for r in records) / num_of_records),
            num_of_records,
        )

    @classmethod
    def get_message_with_average_stats(cls, records):
        avg_infected, num_of_records = cls.get_average_of("infected", records)
        avg_dead, _ = cls.get_average_of("dead", records)
        avg_recovered, _ = cls.get_average_of("recovered", records)

        return cls.average_message_tempalte.format(
            number_of_days=num_of_records,
            avg_daily_infected=avg_infected,
            avg_daily_dead=avg_dead,
            avg_daily_recovered=avg_recovered,
        )

    @commands.command(name="last")
    async def get_the_latest_record(self, ctx):
        record = RecordService.get_the_latest_record()
        msg = self.get_message_for_record(record)
        await ctx.send(msg)

    @commands.command(name="week")
    async def get_records_for_last_7_days(self, ctx):
        records = RecordService.get_n_latest_records()
        msg = self.get_message_with_average_stats(records)

        for record in records:
            msg = msg + self.get_message_for_record(record)
        await ctx.send(msg)
