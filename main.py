import os

from dotenv import load_dotenv

from db.database import Database
from bot.bot import run_bot

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    PREFIX = os.getenv("PREFIX")

    if TOKEN is None:
        print("Provide Discord's Token via TOKEN environment variable!")
        exit()

    Database.connect()

    if PREFIX is not None:
        run_bot(TOKEN, prefix=PREFIX)

    run_bot(TOKEN)

    Database.close_connection()
