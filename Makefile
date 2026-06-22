PYTHON ?= python3
PORT ?= 8000

.PHONY: check serve

check:
	$(PYTHON) -m compileall -q app.py tests
	$(PYTHON) -m unittest discover -s tests

serve:
	PORT=$(PORT) $(PYTHON) app.py
