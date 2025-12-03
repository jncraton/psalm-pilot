all: build

.PHONY: lint lint-fix lint-js lint-py lint-py-fix install build serve clean clean-cache clean-build test

# Run both JS/TS + Python linters
lint: lint-js lint-py

# Fix both JS/TS + Python
lint-fix: lint-js-fix lint-py-fix

# JS/TS lint
lint-js:
	npx prettier@3.6.2 --check .

lint-js-fix:
	npx prettier@3.6.2 --write .

#Python lint
lint-py:
	pipx run --spec ruff==0.13.3 ruff check .

lint-py-fix:
	pipx run --spec ruff==0.13.3 ruff check . --fix

install:
	pip install -r requirements.txt

build:
	python ./build/render.py

serve:
	cd ./www && python -m http.server

clean: clean-cache clean-build

clean-cache:
	rm -rf __pycache__ .pytest_cache .ruff_cache */__pycache__ */.pytest_cache */.ruff_cache

clean-build:
	rm -rf www/index.html www/hymns/* www/service-worker.js www/hymns_list.json

# run test_file tests
test:
	pytest

