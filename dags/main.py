from airflow.decorators import dag
from constants import DAG_ARGS, SCHEDULE_INTERVAL
from tasks.scrape_weather_data import scrape_weather_data
from tasks.train_weather_data import train_weather_data


@dag(
    dag_id="weather_forecast",
    description="Pipeline to scrape and train weather data",
    default_args=DAG_ARGS,
    schedule_interval=SCHEDULE_INTERVAL,
    catchup=False,  # Ensure catchup is set based on your requirements
)
def generate_dag_weather_forecast():
    # Define tasks
    scrape_task = scrape_weather_data()
    train_task = train_weather_data(scrape_task)

    # Set dependencies
    scrape_task >> train_task


generate_dag_weather_forecast()
