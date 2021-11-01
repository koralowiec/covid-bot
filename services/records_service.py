from typing import List, Tuple
from tabulate import tabulate

from db.schemas import Record


class RecordService:
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

    voivodeship_table_headers = [
        "\nWojewództwo",
        "Liczba\nZakażonych",
        "Liczba\ntestów",
        "Pozytywne\ntesty [%]",
    ]

    voivodeship_table_message_template = """Dzienne przyrosty dla województw z {date}:
```
{msg_table}
```
        """

    @staticmethod
    def get_the_latest_record():
        return Record.objects.order_by("-date_of_scrape").first()

    @staticmethod
    def get_n_latest_records(n: int = 7):
        return Record.objects.order_by("-date_of_scrape").limit(n)

    @classmethod
    def prepare_message_for_record(cls, record):
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
    def prepare_message_with_average_stats(cls, records):
        avg_infected, num_of_records = cls.get_average_of("infected", records)
        avg_dead, _ = cls.get_average_of("dead", records)
        avg_recovered, _ = cls.get_average_of("recovered", records)

        return cls.average_message_tempalte.format(
            number_of_days=num_of_records,
            avg_daily_infected=avg_infected,
            avg_daily_dead=avg_dead,
            avg_daily_recovered=avg_recovered,
        )

    @classmethod
    def get_message_for_the_latest_record(cls):
        record = cls.get_the_latest_record()
        print(record.date)
        print(record.id)
        return cls.prepare_message_for_record(record)

    @classmethod
    def get_message_for_average_for_7_days(cls):
        records = cls.get_n_latest_records()
        return cls.prepare_message_with_average_stats(records)

    @classmethod
    def get_message_for_7_days(cls):
        msg = cls.get_message_for_average_for_7_days()

        records = cls.get_n_latest_records()
        for record in records:
            msg = msg + cls.prepare_message_for_record(record)

        return msg

    @classmethod
    def get_table_message_for_latest_record_per_voivodeship(cls) -> str:
        record: Record = cls.get_the_latest_record()

        table: List[Tuple[str, int, int, float]] = []
        for v_stats in record.voivodeships:  # type: ignore
            infected_to_tested_percent = round(
                v_stats.daily.infected / v_stats.daily.tested * 100, 2
            )

            table.append(
                (
                    v_stats.name,
                    v_stats.daily.infected,
                    v_stats.daily.tested,
                    infected_to_tested_percent,
                )
            )

        msg_table = tabulate(table, cls.voivodeship_table_headers, tablefmt="simple")
        msg_table = cls.voivodeship_table_message_template.format(
            date=record.date, msg_table=msg_table
        )
        return msg_table
