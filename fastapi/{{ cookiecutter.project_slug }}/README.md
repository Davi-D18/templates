# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

Stack: FastAPI + SQLAlchemy (async) + Alembic + Pydantic Settings{% if cookiecutter.use_authentication == "yes" %} + JWT auth{% endif %}.

## Requisitos

- Python 3.12+
{%- if cookiecutter.dependency_manager == "poetry" %}
- Poetry
{%- endif %}
{%- if cookiecutter.use_docker == "yes" %}
- Docker + Docker Compose
{%- endif %}

## Setup local

```bash
cp .env.example .env      # ajuste DATABASE_URL e SECRET_KEY
```

Instale as dependências:

{% if cookiecutter.dependency_manager == "poetry" -%}
```bash
poetry install
```
{%- else -%}
```bash
pip install -r requirements-dev.txt
```
{%- endif %}

Prepare o banco e rode:

```bash
make migrate
make run
```

A API sobe em http://localhost:8000/ (health check em `/`).{% if cookiecutter.use_documentation == "yes" %} Documentação em `/docs` e `/redoc`.{% endif %}

## Comandos

| Comando | Descrição |
|---------|-----------|
| `make run` | Servidor de desenvolvimento (uvicorn --reload) |
| `make migrate` | Aplica migrations (Alembic) |
| `make makemigration m="msg"` | Cria migration autogerada |
| `make format` / `make lint` | Ruff |
{%- if cookiecutter.use_tests == "yes" %}
| `make test` | pytest |
{%- endif %}
{%- if cookiecutter.use_docker == "yes" %}
| `make docker-up` | Sobe com docker-compose |
{%- endif %}

## Estrutura

```
{{ cookiecutter.project_slug }}/
├── {{ cookiecutter.project_slug }}/
│   ├── app/
│   │   ├── main.py           # entrypoint (app = create_app())
│   │   ├── models/           # SQLAlchemy{% if cookiecutter.use_authentication == "yes" %} (User){% endif %}
│   │   ├── routers/          # health{% if cookiecutter.use_authentication == "yes" %}, auth, users{% endif %}
│   │   └── schemas/          # Pydantic{% if cookiecutter.use_authentication == "yes" %} (User, auth){% endif %}
│   └── core/
│       ├── configs/          # database, migrations{% if cookiecutter.use_authentication == "yes" %}, security, auth{% endif %}
│       ├── messages/         # mensagens de erro
│       └── settings/         # base / boot / development / production
├── alembic/                  # migrations
├── tests/                    # pytest
├── alembic.ini
├── pyproject.toml
├── requirements.txt          # se dependency_manager=pip
├── Makefile
└── .env.example
```

## Migrations (Alembic)

```bash
make makemigration m="create users"
make migrate
```

## Deploy

- `ENVIRONMENT=production`
- `SECRET_KEY` forte{% if cookiecutter.use_authentication == "yes" %} e `JWT_SECRET_KEY`{% endif %}
- `DATABASE_URL` de produção
- `CORS_ORIGINS`, `CORS_METHODS`, `CORS_HEADERS`, `ALLOWED_HOSTS`

## Licença

{{ cookiecutter.license }}.
