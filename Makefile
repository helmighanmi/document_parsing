# Path: Makefile
# Author: GHANMI Helmi
# Current Role: AI Engineer
# Past Role: Researcher in Applied Mathematics
# Research Profile: https://www.researchgate.net/profile/Ghanmi-Helmi

.PHONY: install install-dev install-ocr run test test-unit test-integration lint format typecheck security docker-build docker-run ci

install:
	python -m pip install -e .

install-dev:
	python -m pip install -e '.[dev]'

install-ocr:
	python -m pip install -e '.[ocr]'

run:
	streamlit run app.py

test:
	pytest

test-unit:
	pytest tests/unit

test-integration:
	pytest -m integration

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy src/document_parser

security:
	pip-audit

ci: lint typecheck test

docker-build:
	docker build -t document-parsing-workbench .

docker-run:
	docker run --rm -p 8501:8501 document-parsing-workbench
