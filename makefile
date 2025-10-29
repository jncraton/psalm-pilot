
.PHONY: lint lint-fix lint-js lint-py lint-py-fix install build clean test

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
	cd data && make install
	pip install -r requirements.txt

build:
	cd data && make
	python render.py

clean:
	cd data && make clean
	rm -rf __pycache__ .pytest_cache .ruff_cache
  
 #run test_file tests
test:
	pytest

