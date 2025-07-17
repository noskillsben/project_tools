#!/usr/bin/env python3
"""
Setup script for project_tools package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read version from __init__.py
init_path = Path(__file__).parent / "__init__.py"
version = "1.0.0"
if init_path.exists():
    with open(init_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('__version__'):
                version = line.split('=')[1].strip().strip('"\'')
                break

setup(
    name="project-tools",
    version=version,
    author="Project Tools Contributors",
    author_email="noreply@projecttools.dev",
    description="Universal project management tools with CLI and web GUI for todo tracking and version management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/project-tools",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Version Control",
        "Topic :: Office/Business :: Scheduling",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies - uses only standard library for core functionality
    ],
    extras_require={
        "web": [
            "Flask>=2.3.0",
            "Flask-CORS>=4.0.0", 
            "Flask-SocketIO>=5.3.0",
            "python-socketio>=5.8.0",
            "python-engineio>=4.7.0",
            "eventlet>=0.33.0",
        ],
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "all": [
            "Flask>=2.3.0",
            "Flask-CORS>=4.0.0", 
            "Flask-SocketIO>=5.3.0",
            "python-socketio>=5.8.0",
            "python-engineio>=4.7.0",
            "eventlet>=0.33.0",
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "project-tools=project_tools.cli:main",
            "project-tools-web=project_tools.web_gui.app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)