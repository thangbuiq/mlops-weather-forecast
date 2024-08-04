# dags/scrape.py

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd

from utils.scrape import WeatherScraper
from constants import SCHEDULE_INTERVAL


def scrape_weather_data():
    scraper = WeatherScraper(
        remote_driver=True,
        remote_url="remote_chromedriver:4444/wd/hub",
    )
    weather_data = scraper.get_latest_weather_data()
    processed_data: pd.DataFrame = scraper.process_weather_data(weather_data)

    # TODO: Upload data to S3

    return None


default_args = {
    "owner": "airflow",
}

dag = DAG(
    "weather_forecast_pipeline",
    default_args=default_args,
    description="Pipeline to scrape and predict weather data",
)

scrape_weather_data_task = PythonOperator(
    task_id="scrape_weather_data",
    python_callable=scrape_weather_data,
    dag=dag,
)
