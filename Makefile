airflow_compose_file := ./docker-compose.airflow.yaml

aup:
	docker-compose -f $(airflow_compose_file) up -d

adown:
	docker-compose -f $(airflow_compose_file) down

arestart:
	make adown && make aup