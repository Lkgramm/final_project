run:
	poetry run uvicorn src.app.main:app --reload

test:
	poetry run pytest

lint:
	poetry run ruff check src tests
