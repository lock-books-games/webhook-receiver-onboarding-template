.PHONY: help setup run

help:
	@echo "Available commands:"
	@echo "  make setup  - install dependencies"
	@echo "  make run    - run the webhook receiver locally"

setup:
	pip install -r requirements.txt

run:
	uvicorn src.app:app --reload --port 8000
