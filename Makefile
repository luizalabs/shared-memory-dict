install:
	@poetry install

install-dev:
	@poetry install --extras "all"

test:
	@poetry run pytest

lint:
	@poetry run flake8 shared_memory_dict
	@poetry run isort --check shared_memory_dict
	@poetry run black --skip-string-normalization --line-length 79 --check shared_memory_dict
	@poetry run mypy shared_memory_dict

coverage:
	@poetry run pytest --cov shared_memory_dict/ --cov-report=term-missing --cov-report=xml
