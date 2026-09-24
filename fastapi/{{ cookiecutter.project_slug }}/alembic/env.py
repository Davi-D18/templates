from alembic import context

from {{ cookiecutter.project_slug }}.core.configs.migrations import (
    run_migrations_offline,
    run_migrations_online,
)

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
