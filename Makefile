RELEASE_TYPE := minor

install:
	@poetry install

install-dev:
	@poetry install --extras "all"

test:
	@poetry run pytest

lint:
	@poetry run flake8 shared_memory_dict
	@poetry run isort --check shared_memory_dict
	@poetry run black --check shared_memory_dict
	@poetry run mypy shared_memory_dict

coverage:
	@poetry run pytest --cov shared_memory_dict/ --cov-report=term-missing --cov-report=xml

release:
	@$(eval VERSION := $(shell poetry version $(RELEASE_TYPE) | cut -d' ' -f6-))
	@git add .
	@git commit -m "Bump a $(RELEASE_TYPE) release to version $(VERSION)"
	@git tag $(VERSION)

release-patch:
	@$(MAKE) release RELEASE_TYPE=patch

release-minor:
	@$(MAKE) release RELEASE_TYPE=minor

release-major:
	@$(MAKE) release RELEASE_TYPE=major
