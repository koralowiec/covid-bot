from mongoengine import (
    Document,
    DateTimeField,
    IntField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    StringField,
)
from mongoengine.fields import BooleanField, EmbeddedDocumentListField, LongField


class NumberOfCases(EmbeddedDocument):
    dead = IntField()
    infected = IntField()
    recovered = IntField()
    tested = StringField()


class VoivodeshipRecord(EmbeddedDocument):
    name = StringField(required=True)
    daily = EmbeddedDocumentField(NumberOfCases)


class Record(Document):
    meta = {"collection": "records"}
    date_of_scrape = DateTimeField(required=True)
    total = EmbeddedDocumentField(NumberOfCases)
    daily = EmbeddedDocumentField(NumberOfCases)
    date = StringField()
    voivodeships = EmbeddedDocumentListField(VoivodeshipRecord)


class PushMessage(Document):
    meta = {"collection": "push_messages"}
    guild = LongField(required=True)
    channel = LongField(required=True)
    is_active = BooleanField(required=True, default=True)
