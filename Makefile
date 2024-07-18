airflow_compose_file := ./airflow.docker-compose.yaml

aup:
	sudo docker compose -f $(airflow_compose_file) up -d

aupb:
	sudo docker compose -f $(airflow_compose_file) up --build -d

adown:
	sudo docker compose -f $(airflow_compose_file) down

arestart:
	make adown && make aup

arestart-b:
	make adown && make aupb