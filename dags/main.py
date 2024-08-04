from airflow.decorators import dag
from constants import DAG_ARGS, SCHEDULE_INTERVAL
from tasks.scrape_weather_data import scrape_weather_data


@dag(
    "weather_forecast",
    description="Pipeline to scrape and predict weather data",
    default_args=DAG_ARGS,
    schedule_interval=SCHEDULE_INTERVAL,
)
def generate_dag_weather_forecast():
    scrape_weather_data_task = scrape_weather_data()
    scrape_weather_data_task


generate_dag_weather_forecast()
