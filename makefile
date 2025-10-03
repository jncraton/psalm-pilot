.PHONY: lint lint-fix lint-js lint-py lint-py-fix

#Run both JS/TS + Python linters
lint: lint-js lint-py

#Fix both JS/TS + Python
lint-fix: lint-js-fix lint-py-fix

#JS/TS lint
lint-js:
	npx prettier@3.6.2 --check .

lint-js-fix:
	npx prettier@3.6.2 --write .

#Python lint
lint-py:
	ruff@0.13.7 check .

lint-py-fix:
	black@25.9.0 .
 