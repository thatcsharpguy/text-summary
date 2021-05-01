test:
	pipenv run pytest --cov=. tests

style:
	pipenv run black .
	pipenv run isort .

lint:
	pipenv run flake8 .
	pipenv run isort . --check-only
	pipenv run black . --check