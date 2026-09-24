.PHONY: install format lint migrate run
{%- if cookiecutter.use_tests == "yes" %}
.PHONY: test
{%- endif %}
{%- if cookiecutter.use_docker == "yes" %}
.PHONY: docker-up docker-build
{%- endif %}

{% if cookiecutter.dependency_manager == "poetry" -%}
install:
	poetry install

run:
	poetry run uvicorn {{ cookiecutter.project_slug }}.app.main:app --reload

migrate:
	poetry run alembic upgrade head

makemigration:
	poetry run alembic revision --autogenerate -m "$(m)"

format:
	poetry run ruff format .
	poetry run ruff check --fix .

lint:
	poetry run ruff check .
{%- if cookiecutter.use_tests == "yes" %}

test:
	poetry run pytest
{%- endif %}
{%- else -%}
install:
	pip install -r requirements-dev.txt

run:
	uvicorn {{ cookiecutter.project_slug }}.app.main:app --reload

migrate:
	alembic upgrade head

makemigration:
	alembic revision --autogenerate -m "$(m)"

format:
	ruff format .
	ruff check --fix .

lint:
	ruff check .
{%- if cookiecutter.use_tests == "yes" %}

test:
	pytest
{%- endif %}
{%- endif %}
{%- if cookiecutter.use_docker == "yes" %}

docker-build:
	docker compose build

docker-up:
	docker compose up --build
{%- endif %}
