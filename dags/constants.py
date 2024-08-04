import os
from datetime import datetime

# NOTE: Selenium configurations
CHROMEDRIVER_PATH = "/opt/airflow/packages/container/chromedriver"
REMOTE_CHROMEDRIVER_URL = "remote_chromedriver:4444/wd/hub"

# NOTE: Airflow DAG configurations
SCHEDULE_INTERVAL = "0 0 * * *"
DAG_ARGS = {
    "owner": "airflow",
    "start_date": datetime.now(),
}

# NOTE: AWS S3 configurations
AWS_S3_BUCKET_NAME = os.environ.get("AWS_S3_BUCKET_NAME")
AWS_CREDENTIALS = {
    "key": os.environ.get("AWS_ACCESS_KEY_ID"),
    "secret": os.environ.get("AWS_SECRET_ACCESS_KEY"),
}
