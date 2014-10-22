DEPS:
	pip freeze > DEPS

.PHONY: run
run:
	./venv-python -O -m gitman