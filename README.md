# MLOps with Airflow

A comprehensive MLOps project using Apache Airflow to automate the scraping, training, and visualization of weather forecast data.

![flow](./docs/README.svg)

## Project Flow

> **Note:** Every logical step in the project is located in `dags/tasks/**` and `dags/utils/**`.

- **Data Scraping**: Daily scraping of weather data for Ho Chi Minh City from [timeanddate.com](https://www.timeanddate.com/weather/vietnam/ho-chi-minh-city) using Apache Airflow and `selenium`.
- **Data Upload**: Upload the processed weather data to an S3 bucket using `s3fs`.
- **Model Training**: Train an RNN model with TensorFlow on AWS SageMaker to predict weather for the upcoming week.
- **Data Visualization**: Visualize the predicted weather data on Tableau.


## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/thangbuiq/weather-forecast-on-aws
cd weather-forecast-on-aws
```

2. Start the Airflow server:
```bash
docker compose up -f docker-compose.airflow.yaml
```

3. Access the Airflow UI at [http://localhost:8080](http://localhost:8080).

> **Note:** You can use the `docs/.env.example` file to create a `.env` file with the necessary environment variables:
> - `AIRFLOW_IMAGE_NAME`: Docker image tag for Airflow (e.g., `slim-2.9.3-python3.10`)
> - `AIRFLOW_UID`: User ID for the Airflow user (e.g., `1000`)
> - `_AIRFLOW_WWW_USER_USERNAME`: Username for accessing the Airflow UI
> - `_AIRFLOW_WWW_USER_PASSWORD`: Password for accessing the Airflow UI
> - `AWS_ACCESS_KEY_ID`: AWS access key
> - `AWS_SECRET_ACCESS_KEY`: AWS secret access key
> - `AWS_S3_BUCKET_NAME`: Name of the S3 bucket

4. Alternatively, you can run:

```bash
make aup
```
> **Note:** This will require `build-essential` to be installed.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please contact [thangbuiq.work@gmail.com](mailto:thangbuiq.work@gmail.com).
