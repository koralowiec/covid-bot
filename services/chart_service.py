import matplotlib.pyplot as plt
import numpy as np
from services.records_service import RecordService
from datetime import datetime


class ChartService:
    record_service = RecordService
    config = [["Infected", "Tested"], ["dead", "infected", "recovered"]]

    @staticmethod
    def grouped_bar_chart(
        labels,
        legend: str = [],
        to_group_1: int = [],
        to_group_2: int = [],
        to_group_3: int = [],
    ):
        x = np.arange(len(labels))
        width = 0.3
        fig, ax = plt.subplots()
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
                if second_layer is not 0:
                    tab_for_append_element.append(second_layer)
        if len(tab_for_append_element) != len(labels):
            tab_for_append_element.append(0)
        return tab_for_append_element

    @classmethod
    def plot_latest_voivodeships(cls):
        record = cls.record_service.get_the_latest_record()
        labels = [name.name for name in record.voivodeships]
        infected = [
            daily_infected.daily.infected for daily_infected in record.voivodeships
        ]
        tested = [daily_tested.daily.tested for daily_tested in record.voivodeships]
        return cls.grouped_bar_chart(labels, cls.config[0], infected, tested)

    @classmethod
    def plot_n_latest_records(
        cls, n: int = 7, voivodeships: str = None, config: str = "total"
    ):
        record = cls.record_service.get_n_latest_records(n)
        labels = [
            datetime.strptime(date.date, "%d.%m.%Y %H:%M").strftime("%m/%d/%Y")
            for date in record
        ]
        if voivodeships:
            infected_to_format = [
                [
                    x.daily["infected"] if x.name == voivodeships else 0
                    for x in voievode.voivodeships
                ]
                for voievode in record
            ]
            tested_to_format = [
                [
                    x.daily["tested"] if x.name == voivodeships else 0
                    for x in voievode.voivodeships
                ]
                for voievode in record
            ]
            # Format the value
            infected = cls.get_list_element(infected_to_format, labels)
            tested = cls.get_list_element(tested_to_format, labels)
            return cls.grouped_bar_chart(labels, cls.config[0], infected, tested)
        else:
            dead = [d_dead[config].dead for d_dead in record]
            infected = [f_infected[config].infected for f_infected in record]
            recovered = [r_recovered[config].recovered for r_recovered in record]
            return cls.grouped_bar_chart(
                labels, cls.config[1], dead, infected, recovered
            )
