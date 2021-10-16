import os

from dotenv import load_dotenv

from db.database import Database
from bot.bot import run_bot

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("TOKEN")

    if TOKEN is None:
        print("Provide Discord's Token via TOKEN environment variable!")
        exit()

    Database.connect()

    run_bot(TOKEN)

    Database.close_connection()
