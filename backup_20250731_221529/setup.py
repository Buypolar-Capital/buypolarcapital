#!/usr/bin/env python3
"""
BuyPolar Capital - Quantitative Finance Research Hub
A comprehensive repository for trading algorithms, market analysis, and educational resources.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="buypolarcapital",
    version="1.0.0",
    author="BuyPolar Capital",
    author_email="your.email@example.com",
    description="Quantitative Finance Research Hub with trading algorithms and market analysis",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/buypolarcapital",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/buypolarcapital/issues",
        "Documentation": "https://yourusername.github.io/buypolarcapital/",
        "Source Code": "https://github.com/yourusername/buypolarcapital",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "pre-commit>=3.3.0",
        ],
        "docs": [
            "sphinx>=7.1.0",
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.2.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "jupyterlab>=4.0.0",
            "ipywidgets>=8.0.0",
        ],
        "gpu": [
            "cupy-cuda11x>=12.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "buypolar=buypolarcapital.cli:main",
            "bpc-dashboard=buypolarcapital.dashboards.cli:main",
            "bpc-quiz=buypolarcapital.quiz.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "buypolarcapital": [
            "assets/**/*",
            "data/**/*",
            "templates/**/*",
        ],
    },
    zip_safe=False,
    keywords=[
        "quantitative finance",
        "trading algorithms",
        "market analysis",
        "risk management",
        "machine learning",
        "financial modeling",
        "backtesting",
        "portfolio optimization",
    ],
) 