# dags/tasks/train_weather_data.py

import os
from datetime import datetime

import pandas as pd
from airflow.decorators import task
from constants import AWS_CREDENTIALS, AWS_S3_BUCKET_NAME, REMOTE_CHROMEDRIVER_URL
from utils.logger import logger
from utils.scrape_weather_data import WeatherScraper
from utils.train_weather_data import time_series_rnn


@task.python(
    show_return_value_in_logs=True,
)
def train_weather_data(s3_url: str):
    # NOTE: Download the weather data from S3
    logger.info("Downloading weather data from S3")
    processed_data = pd.read_csv(
        s3_url,
        storage_options=AWS_CREDENTIALS,
    )

    logger.info(f"Downloaded data shape: {processed_data.shape}")
    print(processed_data)

    # NOTE: Train the weather data by using RNN
    logger.info("Training weather data")
    accuracy_wind, test_data_values_wind, predicted_wind = time_series_rnn(
        df=processed_data,
        column_name="wind_kmh",
        test_size=0.15,
        num_epochs=20,
    )

    logger.info(f"Wind accuracy: {accuracy_wind:.2f}%")

    return accuracy_wind
