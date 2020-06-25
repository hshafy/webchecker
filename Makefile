.PHONY: test shell test-cov up hard-restart logs

test:
	python -m pytest

shell:
	poetry shell

test-cov:
	coverage run --source=webchecker -m pytest
	coverage report

up:
	docker-compose up -d

hard-restart:
	docker-compose up --force-recreate -d --build	

logs:
	docker-compose logs -f
