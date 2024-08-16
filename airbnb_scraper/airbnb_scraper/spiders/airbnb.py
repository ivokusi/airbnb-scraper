import scrapy


class AirbnbSpider(scrapy.Spider):
    name = "airbnb"
    allowed_domains = ["airbnb.com"]
    start_urls = ["https://airbnb.com"]

    def parse(self, response):
        pass
