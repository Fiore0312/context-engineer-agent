#!/usr/bin/env python3
"""
Setup script per Context Engineering Agent
"""

from setuptools import setup, find_packages
from pathlib import Path

# Leggi README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else ""

# Leggi requirements
requirements = [
    "click>=8.0.0",
    "jinja2>=3.0.0",
    "pydantic>=1.8.0",
    "gitpython>=3.1.0",
    "pyyaml>=6.0",
    "rich>=12.0.0",
    "pathspec>=0.9.0"
]

setup(
    name="context-engineer-agent",
    version="1.0.0",
    author="Context Engineering Team",
    author_email="team@contextengineering.dev",
    description="Agente per automazione Context Engineering con Claude Code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/contextengineering/agent",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Tools",
        "Topic :: Software Development :: Code Generators",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
        ],
    },
    entry_points={
        "console_scripts": [
            "context-engineer=cli:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["templates/**/*.md", "templates/**/*.json", "examples/**/*"],
    },
    zip_safe=False,
)