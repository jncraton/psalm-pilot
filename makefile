.PHONY: lint lint-write

lint:
	npx prettier@3.6.2 --check .

lint-write:
	npx prettier@3.6.2 --write .
