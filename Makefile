.PHONY: test shell test-cov

test:
	python -m pytest

shell:
	poetry shell

test-cov:
	coverage run --source=webchecker -m pytest
	coverage report
