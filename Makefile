.PHONE: build
build:
	python3.11 -m venv .venv

.PHONE: install
install:
	pip install -r ./requirements.txt

.PHONE: dev
dev:
	uvicorn kiki_delivery.main:app --reload
