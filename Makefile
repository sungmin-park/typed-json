setup: venv
	venv/bin/pip install -e .[dev]

venv:
	python3.7 -m venv venv
