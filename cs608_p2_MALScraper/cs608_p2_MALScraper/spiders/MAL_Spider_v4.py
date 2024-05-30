import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.signals import spider_closed
import pandas as pd
import csv
import os
import logging
import re
import time

class MalSpider(scrapy.Spider):
    
    target_cols_list = ["anime_id", "synopsis", "image_url"]
    #anime_df = pd.read_csv("../../../data/01_raw/rating.csv")
    anime_df = pd.read_csv("C:/Users/user/My Drive/MITB_AI/Term 5/CS608 Recommender Systems/Project 2/cs608-p2-experiments/data/01_raw/rating.csv")
    MAL_id_list = anime_df["anime_id"].unique()

    name = "MAL_Spider_v4"
    base_url = "https://myanimelist.net/anime"

    def start_requests(self):
        print(f"Starting scraping operation\n")

        # for MAL_id in self.MAL_id_list:
        MAL_id_sublist = self.MAL_id_list[0:5]
        for MAL_id in MAL_id_sublist:
            time.sleep(3)
            
            url = self.base_url + f"/{MAL_id}"

            self.log(f"URL: {url}", level=logging.INFO)
            yield scrapy.Request(url=url, callback=self.parse)
    def __init__(self, *args, **kwargs):
        super(MALSpider, self).__init__(*args, **kwargs)
        self.data = []

    def parse(self, response):

        # Extracting anime_id
        anime_url = response.css('link[href*="https://myanimelist.net/anime/"]::attr(href)').get()
        anime_id = re.search('(?!\/)\d+', anime_url)[0]

        # Extracting synopsis
        synopsis_object = response.css('p[itemprop="description"]::text')
        synopsis = ""
        for i in range(len(synopsis_object)):
            synopsis = synopsis + synopsis_object[i].get()
        # Removing html artifacts from synopsis
        synopsis = re.sub(r"\r\n", " ", synopsis)
        synopsis = re.sub(r"<.*?>"," ", synopsis)

        # Extracting image URL
        img_url = response.css('img[itemprop="image"]::attr(data-src)').get()

        # Initialize dataframe
        df_content = {
            "anime_id": [anime_id],
            "synopsis": [synopsis],
            "img_url": [img_url]
        }
        self.data.append(df_content)        
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(MALSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=spider_closed)
        return spider

    def spider_closed(self, spider):
        # Convert collected data into a DataFrame
        df = pd.DataFrame(self.data)
        # Write the DataFrame to a CSV file
        df_path = "C:/Users/user/My Drive/MITB_AI/Term 5/CS608 Recommender Systems/Project 2/cs608-p2-experiments/data/01_raw/anime_scrapy.csv"
        df.to_csv(df_path, sep="|", index=False)
        print(f"Data saved to {df_path}")


