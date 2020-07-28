install:
	@poetry install

test:
	@pytest

lint:
	@flake8 shared_memory_dict
	@isort --check shared_memory_dict
	@black --skip-string-normalization --line-length 79 --check shared_memory_dict
	@mypy shared_memory_dict

coverage:
	@pytest --cov shared_memory_dict/ --cov-report=term-missing --cov-report=xml
