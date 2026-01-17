# app/crawlers/spiders/basic_spider.py
import scrapy
import hashlib
from datetime import datetime

class BasicSpider(scrapy.Spider):
    name = "basic_spider"
    start_urls = [
        "quotes.toscrape.com", # Example site
        # https://duckduckgo.com, https://dogpile.com, https://surfwax.com, https://search.com, http://bravesearch.com, https://metacrawler.com, https://ixquick.com, https://clusty.com
    ]

    def parse(self, response):
        # Extract data (simple example)
        title = response.css('title::text').get()
        content = ' '.join(response.css('div.quote span.text::text').getall()).strip()
        url = response.url

        if title and content:
            # Yield data to the pipeline
            yield {
                'title': title,
                'content': content,
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'url_hash': hashlib.sha256(url.encode('utf-8')).hexdigest()
            }

        # Follow links to scrape more pages
        next_page_links = response.css('li.next a::attr(href)').getall()
        for link in next_page_links:
            yield response.follow(link, self.parse)


