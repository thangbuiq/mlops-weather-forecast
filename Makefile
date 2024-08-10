airflow_compose_file := './docker-compose.yaml'

aup:
	docker compose -f $(airflow_compose_file) up -d

aupb:
	docker compose -f $(airflow_compose_file) up --build -d

adown:
	docker compose -f $(airflow_compose_file) down

arestart:
	make adown && make aup

arestart-b:
	make adown && make aupb

update:
	docker compose -f $(airflow_compose_file) restart airflow-scheduler
