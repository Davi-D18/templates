import os

os.environ.setdefault("ENVIRONMENT", "development")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
{%- if cookiecutter.use_authentication == "yes" %}
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret")
{%- endif %}
