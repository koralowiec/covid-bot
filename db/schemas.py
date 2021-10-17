from mongoengine import (
    Document,
    DateTimeField,
    IntField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    StringField,
)


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
