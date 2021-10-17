from mongoengine import (
    Document,
    DateTimeField,
    IntField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    StringField,
)
from mongoengine.fields import BooleanField, LongField


class NumberOfCases(EmbeddedDocument):
    dead = IntField()
    infected = IntField()
    recovered = IntField()


class Record(Document):
    meta = {"collection": "records"}
    date_of_scrape = DateTimeField(required=True)
    total = EmbeddedDocumentField(NumberOfCases)
    daily = EmbeddedDocumentField(NumberOfCases)
    date = StringField()


class PushMessage(Document):
    meta = {"collection": "push_messages"}
    guild = LongField(required=True)
    channel = LongField(required=True)
    is_active = BooleanField(required=True, default=True)
