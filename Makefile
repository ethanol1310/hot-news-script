lint:
	poetry run black --diff --color --quiet --check .
	poetry run ruff check .

fmt:
	poetry run black .
	poetry run ruff check --fix .

all: fmt lint

.PHONY: fmt lint
