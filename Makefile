install:
	poetry install

test:
	poetry run pytest --cov=page_loader --cov-report xml tests 

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
