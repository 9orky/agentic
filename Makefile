PYTHON ?= python3
PIPX ?= pipx

.PHONY: dev-refresh test

dev-refresh:
	$(PIPX) install --force --editable .

test:
	$(PYTHON) -m unittest discover -s tests