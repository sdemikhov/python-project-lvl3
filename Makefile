install:
	@poetry install

test:
	poetry run pytest sdemikhov_page_loader tests

lint:
	poetry run flake8 sdemikhov_page_loader

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	@poetry build

publish: build
	@poetry -r test_pypi

.PHONY: install test lint selfcheck check build publish
