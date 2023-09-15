import json

import connect
from src.models import Author, Quote

with open("src/authors.json", "r", encoding="utf-8") as file:
    collection = json.load(file)

for field in collection:
    Author(fullname=field["fullname"],
           born_date=field["born_date"],
           born_location=field["born_location"],
           description=field["description"]).save()

authors = Author.objects()

with open("src/quotes.json", "r", encoding="utf-8") as f:
    collection = json.load(f)

    for quote in collection:
        quotes_obj = Quote.objects(quote=quote['quote'])
        if quotes_obj:
            break

        quote_new = Quote()
        quote_new.quote = quote['quote']
        quote_new.tags = quote['tags']
        authors = Author.objects(fullname=quote['author'])
        if authors:
            quote_new.author = authors[0]
        quote_new.save()