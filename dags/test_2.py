from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

default_args = {"start_date": datetime(2022, 1, 1), "retries": 1}


def sum_task_1_func(**context):
    print_task_1_result = context["ti"].xcom_pull(
        task_ids="print_task_1", key="return_value"
    )
    print_task_2_result = context["ti"].xcom_pull(
        task_ids="print_task_2", key="return_value"
    )
    if print_task_1_result is not None and print_task_2_result is not None:
        result = print_task_1_result + print_task_2_result
        return result


def sum_task_2_func(**context):
    print_task_3_result = context["ti"].xcom_pull(
        task_ids="print_task_3", key="return_value"
    )
    print_task_4_result = context["ti"].xcom_pull(
        task_ids="print_task_4", key="return_value"
    )
    if print_task_3_result is not None and print_task_4_result is not None:
        result = print_task_3_result + print_task_4_result
        return result


def multiplication_task_func(**context):
    sum_task_1_result = context["ti"].xcom_pull(
        task_ids="sum_task_1", key="return_value"
    )
    sum_task_2_result = context["ti"].xcom_pull(
        task_ids="sum_task_2", key="return_value"
    )
    if sum_task_1_result is not None and sum_task_2_result is not None:
        result = sum_task_1_result * sum_task_2_result
        return result


with DAG("test_dag_2", default_args=default_args, schedule_interval=None) as dag:
    input_values = [1, 2, 3, 4]

    sum_task_1 = PythonOperator(
        task_id="sum_task_1",
        python_callable=sum_task_1_func,
        provide_context=True,
    )

    sum_task_2 = PythonOperator(
        task_id="sum_task_2",
        python_callable=sum_task_2_func,
        provide_context=True,
    )

    multiplication_task = PythonOperator(
        task_id="multiplication_task",
        python_callable=multiplication_task_func,
        provide_context=True,
    )

    print_task_1 = PythonOperator(
        task_id="print_task_1",
        python_callable=lambda: input_values[0],
    )

    print_task_2 = PythonOperator(
        task_id="print_task_2",
        python_callable=lambda: input_values[1],
    )

    print_task_3 = PythonOperator(
        task_id="print_task_3",
        python_callable=lambda: input_values[2],
    )

    print_task_4 = PythonOperator(
        task_id="print_task_4",
        python_callable=lambda: input_values[3],
    )

    [print_task_1, print_task_2] >> sum_task_1

    [print_task_3, print_task_4] >> sum_task_2

    [sum_task_1, sum_task_2] >> multiplication_task
