# cs608-p2-experiments
This repository is for the purposes of CS608 Recommender Systems: Project 2 for Group 4. 

Notebooks containing coding artifacts used over the course of the project may be found in the folder "notebooks".

Dataset artifacts (kaggle artifacts, processed and feature engineered artifacts) can be found in the zip folder submission on elearn.

## Instructions for web scraping
1. Run all cells in "cs608-p2-experiments/notebooks/01_data_download.ipynb". This will download the kaggle datasets and split "ratings.csv" into "df_unique_anime_damien.csv", "df_unique_anime_leroy.csv", "df_unique_anime_rosamund.csv" and "df_unique_anime_kenneth.csv"
2. Amend name in line 29 of "cs608-p2-experiments/cs608_p2_MALScraper/cs608_p2_MALScraper/spiders/MAL_Spider_v3_1.py"
3. Ensure you are about to run everything in a virtual enviroment (conda or otherwise) with scrapy installed. You may install a venv using environment.yml (some installation of additional packages may be required).
4. cd from "cs608-p2-experiments" into "cs608-p2-experiments/cs608_p2_MALScraper"
5. run command "scrapy crawl MAL_Spider_v3_1". After some time, "cs608-p2-experiments/data/01_raw/anime_scrapy.csv" be created after scraping has been completed.
6. Amend name of "anime_scrapy.csv" with your name (eg. "anime_scrapy_damien.csv") and upload onto teams.
