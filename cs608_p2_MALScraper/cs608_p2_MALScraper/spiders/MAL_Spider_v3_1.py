import scrapy
import pandas as pd
import os
import re
import time
from scrapy.crawler import CrawlerProcess
from scrapy.signals import spider_closed
import logging

class MalSpider(scrapy.Spider):
    name = "MAL_Spider_v3_1"
    target_cols_list = ["anime_id", "synopsis", "image_url"]
    
    anime_df = pd.read_csv("C:/Users/user/My Drive/MITB_AI/Term 5/CS608 Recommender Systems/Project 2/cs608-p2-experiments/data/01_raw/rating.csv")
    MAL_id_list = anime_df["anime_id"].unique()
    
    base_url = "https://myanimelist.net/anime"

    def __init__(self, *args, **kwargs):
        super(MalSpider, self).__init__(*args, **kwargs)
        self.data = []

    def start_requests(self):
        print(f"Starting scraping operation\n")
        MAL_id_sublist = self.MAL_id_list[0:5]
        for MAL_id in MAL_id_sublist:
            time.sleep(3)
            url = self.base_url + f"/{MAL_id}"
            self.log(f"URL: {url}", level=logging.INFO)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Extracting anime_id
        anime_url = response.css('link[href*="https://myanimelist.net/anime/"]::attr(href)').get()
        anime_id = re.search(r'\d+', anime_url)[0] if anime_url else None

        # Extracting synopsis
        synopsis_object = response.css('p[itemprop="description"]::text')
        synopsis = " ".join(synopsis_object.getall()).strip()
        synopsis = re.sub(r"\r\n", " ", synopsis)
        synopsis = re.sub(r"<.*?>", " ", synopsis)

        # Extracting image URL
        img_url = response.css('img[itemprop="image"]::attr(data-src)').get()

        # Collecting data
        self.data.append({
            "anime_id": anime_id,
            "synopsis": synopsis,
            "image_url": img_url
        })

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(MalSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=spider_closed)
        return spider

    def spider_closed(self, spider):
        df = pd.DataFrame(self.data, columns=self.target_cols_list)
        csv_path = "C:/Users/user/My Drive/MITB_AI/Term 5/CS608 Recommender Systems/Project 2/cs608-p2-experiments/data/01_raw/anime_scrapy.csv"
        
        if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
            existing_df = pd.read_csv(csv_path, sep="|")
            df = pd.concat([existing_df, df], ignore_index=True)
        
        df.to_csv(csv_path, sep="|", index=False)
        print(f"Data saved to {csv_path}")

# Running the crawler process
process = CrawlerProcess()
process.crawl(MalSpider)
process.start()
