DEPS:
	pip freeze > DEPS

.PHONY: run
run:
	./venv-python -m gitman