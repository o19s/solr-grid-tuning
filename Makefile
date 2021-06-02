install:
	poetry install

lint: install
	poetry run flake8 src tests

test: install
	poetry run pytest -vvv

build: lint test
	poetry build
