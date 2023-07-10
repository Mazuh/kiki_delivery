.PHONE: build
build:
	python3.11 -m venv .venv

.PHONE: install
install:
	pip install -r ./requirements.txt

.PHONE: migrate
migrate:
	alembic upgrade head

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

.PHONE: requirements
requirements:
	pip freeze > requirements.txt

.PHONE: migrate_autogen
migrate_autogen:
	alembic revision --autogenerate -m 'my new migration'

.PHONE: migrate_up
migrate_up:
	alembic upgrade +1

.PHONE: migrate_down
migrate_down:
	alembic downgrade -1
