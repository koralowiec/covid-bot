from discord.ext import commands

from db.records_service import RecordService


bot = commands.Bot(command_prefix="!covid ")

record_message_template = """
Dane z {date}
Liczba nowych zakażeń: {daily_infected}
Liczba nowych zgonów: {daily_dead}
Liczba nowych ozdrowień: {daily_recovered}
"""

average_message_tempalte = """
Średnia z {number_of_days} dni:
Zakażeń dziennie: {avg_daily_infected}
"""


def get_message_for_record(record):
    return record_message_template.format(
        date=record.date,
        daily_infected=record.daily.infected,
        daily_dead=record.daily.dead,
        daily_recovered=record.daily.recovered,
    )


def get_message_with_average_infected(records):
    num_of_records = len(records)
    avg = int(sum(r.daily.infected for r in records) / num_of_records)

    return average_message_tempalte.format(
        number_of_days=num_of_records, avg_daily_infected=avg
    )


@bot.command(name="last")
async def get_the_latest_record(ctx):
    record = RecordService.get_the_latest_record()
    msg = get_message_for_record(record)
    await ctx.send(msg)


@bot.command(name="week")
async def get_records_for_last_7_days(ctx):
    records = RecordService.get_n_latest_records()
    msg = get_message_with_average_infected(records)

    for record in records:
        msg = msg + get_message_for_record(record)
    await ctx.send(msg)


def run_bot(token: str):
    print("Starting the bot...")
    bot.run(token)
