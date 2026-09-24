#!/usr/bin/env python
"""Clean up conditional files and finish the generated project."""
import os
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

PROJECT = Path.cwd()

USE_AUTH = "{{ cookiecutter.use_authentication }}"
USE_DOCKER = "{{ cookiecutter.use_docker }}"
USE_TESTS = "{{ cookiecutter.use_tests }}"
DEP_MANAGER = "{{ cookiecutter.dependency_manager }}"
LICENSE = "{{ cookiecutter.license }}"
AUTHOR = {{ cookiecutter.author_name | tojson }}
PROJECT_NAME = {{ cookiecutter.project_name | tojson }}
PROJECT_SLUG = {{ cookiecutter.project_slug | tojson }}

PKG = PROJECT / PROJECT_SLUG


def remove(path):
    target = PROJECT / path
    if target.is_dir():
        shutil.rmtree(target)
    elif target.exists():
        target.unlink()


def handle_authentication():
    if USE_AUTH == "no":
        for path in (
            PKG / "app" / "models" / "users.py",
            PKG / "app" / "routers" / "auth.py",
            PKG / "app" / "routers" / "users.py",
            PKG / "app" / "schemas" / "auth.py",
            PKG / "app" / "schemas" / "users.py",
            PKG / "core" / "configs" / "auth.py",
            PKG / "core" / "configs" / "security.py",
            PKG / "core" / "messages" / "users.py",
            PKG / "core" / "messages" / "jwt.py",
            PROJECT / "tests" / "test_auth.py",
        ):
            if path.exists():
                path.unlink()


def handle_docker():
    if USE_DOCKER == "no":
        for path in (
            "Dockerfile",
            "docker-compose.yml",
            ".dockerignore",
            "scripts/entrypoint.sh",
        ):
            remove(path)
        scripts = PROJECT / "scripts"
        if scripts.is_dir() and not any(scripts.iterdir()):
            scripts.rmdir()


def handle_tests():
    if USE_TESTS == "no":
        remove("tests")


def handle_dependency_manager():
    if DEP_MANAGER == "poetry":
        remove("requirements.txt")
        remove("requirements-dev.txt")


def create_venv():
    if DEP_MANAGER != "pip":
        return
    venv = PROJECT / ".venv"
    python = venv / "bin" / "python"
    print("\nCriando ambiente virtual...")
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
    if os.name == "nt":
        python = venv / "Scripts" / "python.exe"
    subprocess.run(
        [str(python), "-m", "pip", "install", "--upgrade", "pip", "--no-warn-script-location"],
        check=True,
    )
    subprocess.run(
        [str(python), "-m", "pip", "install", "-r", str(PROJECT / "requirements-dev.txt"), "--no-warn-script-location"],
        check=True,
    )


def write_license():
    if LICENSE == "Proprietary":
        return
    year = date.today().year
    if LICENSE == "MIT":
        text = f"""MIT License

Copyright (c) {year} {AUTHOR}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    elif LICENSE == "BSD-3-Clause":
        text = f"""BSD 3-Clause License

Copyright (c) {year}, {AUTHOR}
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED.
"""
    else:
        text = (
            "This project is licensed under the GNU General Public License v3.0.\n"
            "See https://www.gnu.org/licenses/gpl-3.0.txt for the full text.\n"
        )
    (PROJECT / "LICENSE").write_text(text)


def main():
    handle_authentication()
    handle_docker()
    handle_tests()
    handle_dependency_manager()
    write_license()
    create_venv()

    print(
        f"""
Setup completo! Projeto '{PROJECT_NAME}' gerado.

Proximos passos:
  1. cd {PROJECT.name}
  2. cp .env.example .env  (e ajuste as variaveis)
"""
        + (
            "  3. poetry install\n"
            if DEP_MANAGER == "poetry"
            else "  3. pip install -r requirements-dev.txt\n"
        )
        + "  4. make migrate && make run\n\nHappy Coding! :)\n"
    )


if __name__ == "__main__":
    main()
