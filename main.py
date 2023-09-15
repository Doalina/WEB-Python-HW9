import json
import scrapy
from scrapy.crawler import CrawlerProcess



class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    quote_list = []
    author_data_list = []
    authors_list = []

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            self.quote_list.append({
                "tags": quote.css(".tags .tag ::text").getall(),
                "author": quote.css(".author ::text").get().strip(),
                "quote": quote.css(".text ::text").get().strip()
            })
            author_link = quote.xpath("span/a/@href").get()
            yield scrapy.Request(url=self.start_urls[0] + author_link, callback=self.author_parse)
        next_link = response.xpath("//li[@class='next']/a/@href").get()

        if next_link:
                yield scrapy.Request(url=self.start_urls[0] + next_link)
                
        with open('src/quotes.json', 'w') as json_file:
            json.dump(self.quote_list, json_file)  
            
        with open('src/authors.json', 'w') as json_file:
            json.dump(self.author_data_list, json_file)          
 
    def author_parse(self, response):
         for author in response.xpath("/html//div[@class='author-details']"):
            fullname = author.css(".author-title ::text").get().strip()
            if fullname not in self.authors_list:
                self.authors_list.append(fullname)    
                self.author_data_list.append({
                    "fullname": fullname,
                    "born_date": author.css(".author-born-date ::text").get(),
                    "born_location": author.css(".author-born-location ::text").get().strip(),
                    "description": author.css(".author-description ::text").get().strip()
                })
            print(self.author_data_list)
              
              

process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()
