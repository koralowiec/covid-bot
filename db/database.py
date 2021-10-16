import os

from pymongo import MongoClient
from mongoengine import connect
from typing import Union


class Database:
    db: Union[MongoClient, None] = None

    @classmethod
    def connect(cls):
        if cls.db is not None:
            print("Already connected")
            return

        MONGO_HOST = os.getenv("MONGO_HOST")
        MONGO_USER = os.getenv("MONGO_USER")
        MONGO_PASS = os.getenv("MONGO_PASS")

        if MONGO_HOST is None or MONGO_USER is None or MONGO_PASS is None:
            print(
                "Provide MongoDB Connection information via MONGO_URL, MONGO_USER, MONGO_PASS environment variables!"
            )
            exit()

        cls.db = connect(host=MONGO_HOST, username=MONGO_USER, password=MONGO_PASS)
        print(f"Connected to host: {MONGO_HOST}")

    @classmethod
    def close_connection(cls):
        if cls.db is None:
            print("Not connected to any database")
            return

        cls.db.close()
