PROJECT_NAME = chargeapi
TEST_FOLDER = tests
APPLICATION = chargeapi.main:app

.PHONY:default
default: help

.PHONY: help
help:
	@echo "All Commands:"
	@echo "	Code Style:"
	@echo "		check - Check format style."
	@echo "		format - Format code style."
	@echo "		typecheck - Check types in code"
	@echo "	Env:"
	@echo "		clean - Remove temp files."
	@echo "		down - Stop containers."
	@echo "		run - Run application in development mode."
	@echo "		unit-test - Run unit tests."
	@echo "		integration-test - Run integration tests."
	@echo "		coverage - Run tests and gather coverage data."
	@echo "		up - Start containers."
	@echo "		start_seed_db - Start seed database."


.PHONY: format
format:
	@echo ""
	@echo "FORMATTING CODE:"
	@echo ""
	black -l 88 -t py310 --skip-string-normalization --preview $(PROJECT_NAME) $(TEST_FOLDER)
	unify --in-place --recursive --quote '"' $(PROJECT_NAME) $(TEST_FOLDER)
	isort --profile black .

	@echo ""
	@echo "CHECKING CODE STILL NEEDS FORMATTING:"
	@echo ""
	black -l 88 -t py310 --skip-string-normalization --preview --check $(PROJECT_NAME) $(TEST_FOLDER)

	@echo ""
	@echo "CHECKING TYPING"
	@echo ""
	@make typecheck

	@echo ""
	@echo "CHECKING CODE STYLE"
	@echo ""
	flake8 $(PROJECT_NAME) $(TEST_FOLDER)

	@echo ""
	@echo "ENSURE DOUBLE QUOTES"
	@echo ""
	unify --check-only --recursive --quote '"' $(PROJECT_NAME) $(TEST_FOLDER)

	@echo ""
	@echo "SORT IMPORTS"
	@echo ""
	isort --profile black -c .

	@echo ""
	@echo "CHECKING SECURITY ISSUES"
	@echo ""
	bandit -r $(PROJECT_NAME)

.PHONY: clean
clean:
	- @find . -name "*.pyc" -exec rm -rf {} \;
	- @find . -name "__pycache__" -delete
	- @find . -name "*.pytest_cache" -exec rm -rf {} \;
	- @find . -name "*.mypy_cache" -exec rm -rf {} \;

.PHONY: typecheck
typecheck:
	mypy --python-version 3.10 --ignore-missing-imports --disallow-untyped-defs --disallow-untyped-calls $(PROJECT_NAME)/

.PHONY: run
run:
	uvicorn $(APPLICATION)

.PHONY: up
up:
	docker-compose up

.PHONY: down
down:
	docker-compose down --remove-orphans

.PHONY: db_upgrade_test
db_upgrade_test:
	DB_PORT=5435 DB_USER=postgres DB_PASS=chargeapi_test DB_HOST=127.0.0.1 DB_PORT=5435 DB_NAME=chargeapi_test alembic upgrade head

.PHONY: unit-test
unit-test:
	pytest tests/unit/ -vv

.PHONY: db_upgrade
db_upgrade:
	alembic upgrade head

.PHONY: db_generate_revision
db_generate_revision:
	alembic revision --autogenerate

.PHONY: integration-test
integration-test:
	- @make db_test_drop
	docker run -d --name chargeapi_test_db -e "POSTGRES_DB=chargeapi_test" -e "POSTGRES_PASSWORD=chargeapi_test" -P -p 127.0.0.1:5435:5432 postgres:14-alpine
	sleep 6
	@make db_upgrade_test
	pytest tests/integration/ -vv
	docker container stop chargeapi_test_db
	docker container rm chargeapi_test_db

.PHONY: coverage
coverage:
	coverage run -m pytest tests/unit/ -vv
	coverage report -m

.PHONY: db_test_drop
db_test_drop:
	docker container ls -a | grep chargeapi_test_db | awk '{print $$1}' | xargs docker container stop | xargs docker container rm

.PHONY: db_drop
db_drop:
	docker container ls -a | grep chargeapi_db | awk '{print $$1}' | xargs docker container stop | xargs docker container rm

.PHONY: start_seed_db
start_seed_db:
	docker-compose -f ../seed/docker-compose.yml up 

.PHONY: run_local_container
run_local_container:
	docker-compose run --service-ports --rm chargeapi_app uvicorn chargeapi.main:app --host 0.0.0.0 --reload
