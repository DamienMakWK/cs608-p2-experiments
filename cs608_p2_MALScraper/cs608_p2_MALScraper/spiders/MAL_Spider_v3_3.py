import scrapy
import pandas as pd
import os
import re
import time
from random import randrange
from scrapy.crawler import CrawlerProcess
from scrapy.signals import spider_closed
import logging

class MalSpider(scrapy.Spider):
    name = "MAL_Spider_v3_3"
    target_cols_list = [
        "anime_id", 
        "synopsis", 
        "image_url", 
        "rating", 
        "va_list", 
        "staff_list",
        # "recommended_review",
        # "mixedfeelings_review",
        # "notrecommended_review",
        "recommended_review_count",
        "mixedfeelings_review_count",
        "notrecommended_review_count"
        ]
    
    # Update user variable with your name ["NA","damien", "leroy", "rosamund", "kenneth"]
    user = "retry"
    data_dir = "C:/Users/user/My Drive/MITB_AI/Term 5/CS608 Recommender Systems/Project 2/cs608-p2-experiments/data/01_raw/"
    if user == "NA":
        rating_csv_filepath = f"{data_dir}rating.csv"
    elif user== "retry":
        rating_csv_filepath = f"{data_dir}missing_anime.csv"
    else:
        rating_csv_filepath = f"{data_dir}rating_{user}.csv"
    
    anime_df = pd.read_csv(rating_csv_filepath)
    MAL_id_list = anime_df["anime_id"].unique()
    print(f"Length of MAL_id_list = {len(MAL_id_list)}, user = {user}")

    base_url = "https://myanimelist.net/anime"

    def __init__(self, *args, **kwargs):
        super(MalSpider, self).__init__(*args, **kwargs)
        self.data = []

    def start_requests(self):
        self.log(f"Starting scraping operation\nAttempting to scrape {len(self.MAL_id_list)} pages", level=logging.INFO)

        for MAL_id in self.MAL_id_list:
            time.sleep(randrange(3,10))
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

        # Extracting rating (eg. R-17+)
        rating = response.xpath('//span[@class="dark_text" and contains(text(), "Rating:")]/following-sibling::text()').get().strip()

        # Extracting voice actors 
        # va_list = response.css('td.va-t.ar.pl4.pr4 a::text').getall()
        va_list = []

        # Extracting staff members
        # Tried response.css('div.detail-characters-list.clearfix div.left-column.fl-l.divider')[1].get() and gotten CSS segment with staff members
        # Able to pull image alt text for last 4 images in "Characters & Voice Actors, Staff", which tend to be staff members
            # Syntax: 
                # response.css('a.fw-n img::attr(alt)')[-1].get()   ;   Returns: 'Irie, Yasuhiro'
                # response.css('a.fw-n img::attr(alt)')[-2].get()   ;   Returns: 'Yonai, Noritomo'
                # response.css('a.fw-n img::attr(alt)')[-3].get()   ;   Returns: 'Maruyama, Hiroo'
                # response.css('a.fw-n img::attr(alt)')[-4].get()   ;   Returns: 'Cook, Justin'
        # Sucessful run:
        # # Get 2nd html object with 'div.detail-characters-list.clearfix' (first html object would contain characters & voice actors)
        # staff_html_obj = response.css('div.detail-characters-list.clearfix')[1]
        # Get all staff names. Example output:
        # ['\n            ',
        #  '\n          ',
        #  'Cook, Justin',
        #  '\n            ',
        #  '\n          ',
        #  'Maruyama, Hiroo',
        #  '\n            ',
        #  '\n          ',
        #  'Yonai, Noritomo',
        #  '\n            ',
        #  '\n          ',
        #  'Irie, Yasuhiro']
        # unclean_staff_list = staff_html_obj.css("a::text").getall()
        # # Removing list elements that start with '\n'
        # regex = re.compile('\\n')
        # clean_staff_list = [i for i in unclean_staff_list if not regex.search(i)]
        clean_staff_list = []
            
        # # Extracting user reviews
        # review_tag_objects = response.css('div.review-element.js-review-element div.tag')
        # reviews = response.css('div.review-element.js-review-element div.text').getall()
        # recommended_review = "Missing review"
        # mixedfeelings_review = "Missing review"
        # notrecommended_review = "Missing review"

        # if len(review_tag_objects) > 1:
        #     for i in len(review_tag_objects):
        #         if review_tag_objects[i].attrib['data-id'] == '1':
        #             recommended_review = reviews[i]
        #         elif review_tag_objects[i].attrib['data-id'] == '2':
        #             mixedfeelings_review = reviews[i]
        #         elif review_tag_objects[i].attrib['data-id'] == '3':
        #             notrecommended_review = reviews[i]
        # else:
        #     if response.css('div.review-element.js-review-element div.tag').attrib['data-id'] == '1':
        #         recommended_review = reviews
        #     elif response.css('div.review-element.js-review-element div.tag').attrib['data-id'] == '2':
        #         mixedfeelings_review = reviews
        #     elif response.css('div.review-element.js-review-element div.tag').attrib['data-id'] == '3':
        #         notrecommended_review = reviews
        # # Review text cleanup
        # recommended_review = re.sub(r"\r\n", " ", recommended_review)
        # recommended_review = re.sub(r"\n", " ", recommended_review)
        # recommended_review = re.sub(r"<.*?>", " ", recommended_review)
        # recommended_review = re.sub(r"\s{2,}", "", recommended_review)

        # mixedfeelings_review = re.sub(r"\r\n", " ", mixedfeelings_review)
        # mixedfeelings_review = re.sub(r"\n", " ", mixedfeelings_review)
        # mixedfeelings_review = re.sub(r"<.*?>", " ", mixedfeelings_review)
        # mixedfeelings_review = re.sub(r"\s{2,}", " ", mixedfeelings_review)

        # notrecommended_review = re.sub(r"\r\n", " ", notrecommended_review)
        # notrecommended_review = re.sub(r"\n", " ", notrecommended_review)
        # notrecommended_review = re.sub(r"<.*?>", " ", notrecommended_review)
        # notrecommended_review = re.sub(r"\s{2,}", " ", notrecommended_review)

        # Extracting # of each review type (recommended, mixed feelings, not recommended)
        recommended_review_count = int(response.css('div.review-ratio__bar').attrib['data-recommended'])
        mixedfeelings_review_count = int(response.css('div.review-ratio__bar').attrib['data-mixed_feeling'])
        notrecommnded_review_count = int(response.css('div.review-ratio__bar').attrib['data-not_recommended'])

        # Collecting data
        self.data.append({
            "anime_id":anime_id,
            "synopsis":synopsis,
            "image_url":img_url,
            "rating":rating,
            "va_list":va_list,
            "staff_list":clean_staff_list,
            # "recommended_review":recommended_review,
            # "mixedfeelings_review":mixedfeelings_review,
            # "notrecommended_review":notrecommended_review,
            "recommended_review_count":recommended_review_count,
            "mixedfeelings_review_count":mixedfeelings_review_count,
            "notrecommended_review_count":notrecommnded_review_count
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
