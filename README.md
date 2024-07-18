# MLOps with Airflow

A simple MLOps project using Apache Airflow to automate the training and deployment of a machine learning model.

## Getting Started

1. Clone the repository
2. Start the Airflow server

> [!NOTE]
> You can following the `.env.example` file to create a `.env` file with the necessary environment variables:
> - `AIRFLOW_IMAGE_NAME`: I used `slim-2.9.3` tag of the `apache/airflow` image
> - `_AIRFLOW_WWW_USER_USERNAME`: username to access the Airflow UI
> - `_AIRFLOW_WWW_USER_PASSWORD`: password to access the Airflow UI

```bash
docker compose up -f docker-compose.airflow.yaml

# Access the Airflow UI at http://localhost:8080, or run:
make aup # this will require build-essential
```