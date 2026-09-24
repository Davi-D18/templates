FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production

WORKDIR /app

{%- if cookiecutter.dependency_manager == "poetry" %}
RUN pip install --no-cache-dir "poetry>=2.0.0"
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --only main --no-root
{%- else %}
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
{%- endif %}

COPY . .
RUN chmod +x scripts/*.sh

EXPOSE 8000
CMD ["./scripts/entrypoint.sh"]
