install:
	poetry install

test:
	poetry run pytest page_loader tests

lint:
	poetry run flake8 page_loader

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	poetry build

publish: build
	poetry publish -r test_pypi

.PHONY: install test lint selfcheck check build publish
