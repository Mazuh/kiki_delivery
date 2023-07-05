.PHONE: build
build:
	python3.11 -m venv .venv

.PHONE: install
install:
	pip install -r ./requirements.txt

.PHONE: dev
dev:
	uvicorn kiki_delivery.application.web:app --reload

.PHONE: types
types:
	pyright

.PHONE: test
test:
	pytest

.PHONE: pyclean
pyclean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

