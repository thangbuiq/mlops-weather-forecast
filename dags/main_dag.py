# dags/main_dag.py
# NOTE: This is the main DAG file that orchestrates the tasks

from airflow import DAG
from constants import DAG_ARGS, SCHEDULE_INTERVAL
from tasks.scrape_weather_data import scrape_weather_data
from tasks.train_weather_data import train_weather_data

with DAG(
    dag_id="weather_forecast",
    description="Pipeline to scrape and train weather data",
    default_args=DAG_ARGS,
    schedule_interval=SCHEDULE_INTERVAL,
    catchup=False,  # Ensure catchup is set based on your requirements
):
    # Define tasks
    scrape_task = scrape_weather_data()
    train_task = train_weather_data(scrape_task)

    # Set dependencies
    scrape_task >> train_task
