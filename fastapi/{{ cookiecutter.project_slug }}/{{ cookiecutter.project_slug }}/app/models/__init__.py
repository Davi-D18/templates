from {{ cookiecutter.project_slug }}.core.configs.database import BaseModel

{% if cookiecutter.use_authentication == "yes" %}from .users import User

{% endif %}__all__ = ["BaseModel"{% if cookiecutter.use_authentication == "yes" %}, "User"{% endif %}]
