#!/usr/bin/env python3
"""
BuyPolar Capital - Quantitative Finance Research Hub
"""

from setuptools import setup, find_packages

def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="buypolarcapital",
    version="2.0.0",
    author="BuyPolar Capital",
    description="Interactive Quantitative Finance Research Hub",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/buypolarcapital",
    packages=find_packages(include=['core*', 'assets*']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "buypolar=core.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
