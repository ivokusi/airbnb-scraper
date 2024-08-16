import scrapy
import json
import re

class AirbnbSpider(scrapy.Spider):
    
    name = "airbnb"

    location = "Virginia--United-States"
    
    checkin = "2024-08-16"
    checkout = "2024-08-20"
    
    adults = "2"
    children = "0"
    infants = "0"
    pets = "0"

    base_url = f"https://www.airbnb.com/s/{location}/homes?checkin={checkin}&checkout={checkout}&adults={adults}&children={children}&infants={infants}&pets={pets}"
    
    def start_requests(self):
        
        yield scrapy.Request(url=self.base_url, callback=self.parse)

    def parse(self, response):
        
        data = response.xpath("//script[@id='data-deferred-state-0']/text()").get()
        jsdata = json.loads(data)

        results = jsdata["niobeMinimalClientData"][0][1]["data"]["presentation"]["staysSearch"]["results"]["searchResults"]
        
        for result in results:

            full_url = f"https://www.airbnb.com/rooms/{result["listing"]["id"]}?checkin={self.checkin}&checkout={self.checkout}&adults={self.adults}&children={self.children}&infants={self.infants}&pets={self.pets}" 
            avg_rating = result["listing"]["avgRatingA11yLabel"]
            
            images = list()
            options = list()
            
            for res in result["listing"]["contextualPictures"]:
                
                images.append(res["picture"])

                if res.get("caption", None) is not None and res["caption"].get("messages", None) is not None:

                    for message in res["caption"]["messages"]:

                        options.append(message)
            
            room_id = result["listing"]["id"]
            title = f"{result["listing"]["name"]} {result["listing"]["title"]}"
            price_per_night = result["pricingQuote"]["structuredStayDisplayPrice"]["primaryLine"]["accessibilityLabel"]
            total_price = result["pricingQuote"]["structuredStayDisplayPrice"]["secondaryLine"]["accessibilityLabel"]
            coordinates = f"latitude: {result["listing"]["coordinate"]["latitude"]} longitude: {result["listing"]["coordinate"]["longitude"]}"

            yield {
                "full_url": full_url,
                "avg_rating": avg_rating,
                "images": images,
                "options": options,
                "room_id": room_id,
                "title": title,
                "price_per_night": price_per_night,
                "total_price": total_price,
                "coordinates": coordinates
            }

            next_page_cursor = jsdata["niobeMinimalClientData"][0][1]["data"]["presentation"]["staysSearch"]["results"]["paginationInfo"]["nextPageCursor"]

            if next_page_cursor:

                next_page_url = f"{self.base_url}&pagination_search=true&cursor={next_page_cursor}"
                yield scrapy.Request(url=next_page_url, callback=self.parse)
