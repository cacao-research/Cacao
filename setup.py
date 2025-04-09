from setuptools import setup, find_packages
import pathlib

# Get the directory containing this file
HERE = pathlib.Path(__file__).parent

# Read the README file
long_description = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="cacao",
    version='1.0.23',
    description="Cacao is a high-performance, reactive web framework for Python, designed to simplify building interactive dashboards and data apps.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Juan Denis",
    author_email="Juan@vene.co",
    python_requires=">=3.7",
    url="https://github.com/jhd3197/Cacao",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(include=['cacao', 'cacao.*']),
    package_data={
        'cacao': [
            'core/static/*.html',
            'core/static/css/*.css',
            'core/static/js/*.js',
            'core/static/icons/*.svg',
            'cli/templates/**/*'
        ]
    },
    include_package_data=True,
    install_requires=[
        "websockets",
        "asyncio",
        "watchfiles",
        "colorama",
        "pywebview>=4.0.2",
    ],
    entry_points={
        "console_scripts": [
            "cacao=cacao.cli:run_cli",
        ],
    },
)