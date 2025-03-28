from setuptools import setup, find_packages

setup(
    name="cacao",
    version='0.0.1',
    description="Cacao is a high-performance, reactive web framework for Python, designed to simplify building interactive dashboards and data apps.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Juan Denis",
    author_email="Juan@vene.co",
    python_requires=">=3.7",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
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