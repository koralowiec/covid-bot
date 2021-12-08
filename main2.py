from services.records_service import RecordService
from services.chart_service import ChartService
import os

from dotenv import load_dotenv

from db.database import Database

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    PREFIX = os.getenv("PREFIX")

    if TOKEN is None:
        print("Provide Discord's Token via TOKEN environment variable!")
        exit()

    Database.connect()
    
    y = ChartService
    #usage
    #y.plot_latest_voivodeships()
    #  voivodeships_name = voivodeships
    #  config_option is only available if voivodeships_name is empty. config_option: total or daily, default on total
    #y.plot_n_latest_records(3,'voivodeships_name','config_option')
    
