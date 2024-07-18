airflow_compose_file := ./airflow.docker-compose.yaml

aup:
	sudo docker compose -f $(airflow_compose_file) up -d

adown:
	sudo docker compose -f $(airflow_compose_file) down

arestart:
	make adown && make aup