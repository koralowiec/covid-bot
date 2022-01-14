import matplotlib.pyplot as plt
import numpy as np
from typing import List
from services.records_service import RecordService
from datetime import datetime


class ChartService:
    record_service = RecordService
    config = [["Infected", "Tested"], ["dead", "infected", "recovered"]]

    @staticmethod
    def grouped_bar_chart(
        labels,
        legend: List[str] = [],
        to_group_1: List[int] = [],
        to_group_2: List[int] = [],
        to_group_3: List[int] = [],
    ):
        x = np.arange(len(labels))
        width = 0.3
        _, ax = plt.subplots()
        if to_group_1:
            plt.bar(x - 0.2, to_group_1, width, color="cyan")
        if to_group_2:
            plt.bar(x, to_group_2, width, color="orange")
        if to_group_3:
            plt.bar(x + 0.2, to_group_3, width, color="red")
        ax.ticklabel_format(style="plain")
        plt.xticks(x, labels, rotation=90)
        plt.legend(legend)

        return plt.savefig("plot.png", bbox_inches="tight")

    @staticmethod
    def get_list_element(list, labels):
        tab_for_append_element = []
        for first_layer in list:
            for second_layer in first_layer:
                if second_layer != 0:
                    tab_for_append_element.append(second_layer)
        if len(tab_for_append_element) != len(labels):
            tab_for_append_element.append(0)
        return tab_for_append_element

    @staticmethod
    def sign_draw_chart(
        labels,
        legend: List[str] = [],
        to_group_1: List[int] = [],
        to_group_2: List[int] = [],
        to_group_3: List[int] = [],
    ):
        _, ax = plt.subplots()
        ax.ticklabel_format(style="plain")
        if to_group_1:
            plt.plot(labels, to_group_1, "go")
        if to_group_2:
            plt.plot(labels, to_group_2, "b<")
        if to_group_3:
            plt.plot(labels, to_group_2, "r>")

        plt.xticks(rotation=90)
        plt.legend(legend)
        return plt.savefig("plot.png", bbox_inches="tight")

    @classmethod
    def plot_latest_voivodeships(cls, chart: str = ""):

        record = cls.record_service.get_the_latest_record()
        labels = [name.name for name in record.voivodeships]
        infected = [
            daily_infected.daily.infected for daily_infected in record.voivodeships
        ]
        tested = [daily_tested.daily.tested for daily_tested in record.voivodeships]
        if chart:
            return cls.sign_draw_chart(labels, cls.config[0], infected, tested)
        else:
            return cls.grouped_bar_chart(labels, cls.config[0], infected, tested)

    @classmethod
    def plot_n_latest_records(
        cls,
        n: int = 7,
        voivodeship_name: str = None,
        chart: bool = False,
        config: str = "daily",
    ):
        records = cls.record_service.get_n_latest_records(n)
        records = [r for r in records]
        records.reverse()
        labels = [
            datetime.strptime(date.date, "%d.%m.%Y %H:%M").strftime("%m/%d/%Y")
            for date in records
        ]

        if voivodeship_name:
            infected_to_format = [
                [
                    x.daily["infected"] if x.name == voivodeship_name else 0
                    for x in voievode.voivodeships
                ]
                for voievode in records
            ]
            tested_to_format = [
                [
                    x.daily["tested"] if x.name == voivodeship_name else 0
                    for x in voievode.voivodeships
                ]
                for voievode in records
            ]

            # Format the value
            infected = cls.get_list_element(infected_to_format, labels)
            tested = cls.get_list_element(tested_to_format, labels)
            if chart:
                return cls.sign_draw_chart(labels, cls.config[0], infected, tested)
            else:
                return cls.grouped_bar_chart(labels, cls.config[0], infected, tested)

        dead = [d_dead[config].dead for d_dead in records]
        infected = [f_infected[config].infected for f_infected in records]
        recovered = [r_recovered[config].recovered for r_recovered in records]

        if chart:
            return cls.sign_draw_chart(labels, cls.config[1], dead, infected, recovered)
        else:
            return cls.grouped_bar_chart(
                labels, cls.config[1], dead, infected, recovered
            )
