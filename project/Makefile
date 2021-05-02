test:
	pipenv run pytest -k "not unit"  --cov=. tests
	pipenv run pytest -k "unit" -n auto

style:
	pipenv run black .
	pipenv run isort .

lint:
	pipenv run flake8 .
	pipenv run isort . --check-only
	pipenv run black . --check