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
def test_predict_weather_data(s3_url: str):
    # NOTE: Download the weather data from S3
    logger.info("Downloading weather data from S3")
    processed_data = pd.read_csv(
        s3_url,
        storage_options=AWS_CREDENTIALS,
    )

    logger.info("Downloaded data: \n", processed_data)

    # NOTE: Predict the weather data

    return None
