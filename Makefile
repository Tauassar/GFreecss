.DEFAULT: help
.PHONY: help bootstrap lint isort test testreport deptree clean

VENV=venv
PYTHON=$(VENV)/bin/python3

help:
	@echo "Please use \`$(MAKE) <target>' where <target> is one of the following:"
	@echo "  bootstrap  - setup packaging dependencies and initialize venv"
	@echo "  start_example      - start_dev server with gunicorn"

bootstrap: $(VENV)/bin/activate
$(VENV)/bin/activate:
	python3.9 -m venv $(VENV)
	$(PYTHON) -m pip install -r requirements/local.txt

start_example: bootstrap
	$(PYTHON) -m gunicorn example_app:app --reload --bind localhost:8001

deptree: bootstrap
	$(PYTHON) -m pipdeptree
