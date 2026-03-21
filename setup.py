#!/usr/bin/env python3
"""
Ludwig Framework Setup
"""

from setuptools import setup, find_packages
import os

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name="ludwig-framework",
    version="0.1.0",
    description="A Python web framework with Laravel-style elegance",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    author="NanaBright",
    url="https://github.com/NanaBright/ludwig",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ludwig=cli.artisan:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
    ],
    keywords="programming-language web desktop framework",
    include_package_data=True,
    zip_safe=False,
)
