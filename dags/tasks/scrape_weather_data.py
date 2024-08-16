# dags/scrape.py

import os
from datetime import datetime

import pandas as pd
from airflow.decorators import task
from constants import AWS_CREDENTIALS, AWS_S3_BUCKET_NAME, REMOTE_CHROMEDRIVER_URL
from utils.logger import logger
from utils.scrape_weather_data import WeatherScraper


@task.python(
    show_return_value_in_logs=True,
)
def scrape_weather_data():
    # NOTE: Scrapes weather data and processes it to a DataFrame
    scraper = WeatherScraper(
        remote_driver=True,
        remote_url=REMOTE_CHROMEDRIVER_URL,
    )
    weather_data = scraper.get_latest_weather_data()
    processed_data: pd.DataFrame = scraper.process_weather_data(weather_data)

    # NOTE: Upload the processed data to S3
    logger.info("Uploading weather data to S3")
    weather_date_range = scraper.get_15_latest_range()
    weather_data_path = f"{weather_date_range}/weather_data.csv"
    weather_data_url = f"s3://{AWS_S3_BUCKET_NAME}/{weather_data_path}"
    processed_data.to_csv(
        weather_data_url,
        storage_options=AWS_CREDENTIALS,
        index=False,
    )

    logger.info("Weather data uploaded to S3")
    return weather_data_url
