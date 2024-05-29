import scrapy
import pandas as pd
import csv
import os
import logging
import re
import time

class MalSpiderSpider(scrapy.Spider):
    target_cols_list = ["anime_id", "synopsis", "image_url"]
    #anime_df = pd.read_csv("../../../data/01_raw/rating.csv")
    anime_df = pd.read_csv("C:/Users/user/My Drive/MITB_AI/Term 5/CS608 Recommender Systems/Project 2/cs608-p2-experiments/data/01_raw/rating.csv")
    MAL_id_list = anime_df["anime_id"].unique()
    

    name = "MAL_Spider"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    allowed_domains = ["myanimelist.net"]
    # start_urls = ["https://myanimelist.net/anime/"]
    base_url = "https://myanimelist.net/anime"

    #output_directory = "../../../data/01_raw/"
    output_directory = "C:/Users/user/My Drive/MITB_AI/Term 5/CS608 Recommender Systems/Project 2/cs608-p2-experiments/data/01_raw"
    os.makedirs(output_directory, exist_ok=True)

    def start_requests(self):
        print(f"Starting scraping operation\n")

        output_file = self.output_directory + "/anime_scrapy.csv"
        
        with open(output_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter="|")
            writer.writerow(self.target_cols_list)

        for MAL_id in self.MAL_id_list:
            time.sleep(1)
            
            url = self.base_url + f"/{MAL_id}"

            self.log(f"URL: {url}", level=logging.INFO)
            
            yield scrapy.Request(url=url, callback=self.parse, meta={"output_file":output_file})

    def parse(self, response):
        # Extracting anime_id
        anime_url = response.css('link[href*="https://myanimelist.net/anime/"]::attr(href)').get()
        anime_id = re.search('(?!\/)\d+', anime_url)[0]

        # Extracting synopsis
        synopsis_object = response.css('p[itemprop="description"]::text')
        synopsis = ""
        for i in range(len(synopsis_object)):
            synopsis = synopsis + synopsis_object[i].get()

        # Extracting image URL
        img_url = response.css('img[itemprop="image"]::attr(data-src)').get()

        yield{
            "anime_id": anime_id,
            "synopsis": synopsis,
            "img_url": img_url
        }


