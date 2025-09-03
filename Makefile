# Makefile to automate the execution of the database documentation script.
# Usage:
# make run DB_CONTAINER=<container_name> DB_USER=<username> DB_PASS=<password> DB_NAME=<db_name>
# Or, set these as environment variables before running:
# export DB_CONTAINER=<container_name>
# export DB_USER=<username>
# export DB_PASS=<password>
# export DB_NAME=<db_name>
# make run

.PHONY: run

run:
	@echo "Executing the database documentation script..."
	python3 main.py --db_container=$(DB_CONTAINER) --db_user=$(DB_USER) --db_pass=$(DB_PASS) --db_name=$(DB_NAME)
