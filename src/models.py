from mongoengine import Document, CASCADE
from mongoengine.fields import ListField, StringField, ReferenceField


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(max_length=30)
    born_location = StringField(max_length=100)
    description = StringField()


class Quote(Document):
    tags = ListField(StringField(max_length=50))
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField(max_length=150, required=True)