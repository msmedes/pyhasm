format:
		@black ./hasm

lint:
		@flake8 hasm tests
		@pylint hasm tests

run:
		@python assembler --filename test.py

test:
		@pytest tests

typecheck:
		@mypy .
