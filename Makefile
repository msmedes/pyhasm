lint:
		@flake8 src tests
		@pylint src tests

run:
		@python assembler --filename test.py

test:
		@pytest tests

typecheck:
		@mypy .
