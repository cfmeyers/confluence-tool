#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = ["Click>=6.0", "atlassian-python-api", "beautifulsoup4"]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest",
]

setup(
    author="Collin Meyers",
    author_email="cfmeyers@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    description="A tool for dealing with Confluence on the command line",
    entry_points={
        "console_scripts": [
            "confluence-tool=confluence_tool.cli:cli",
        ],
    },
    install_requires=requirements,
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="confluence_tool",
    name="confluence_tool",
    packages=find_packages(include=["confluence_tool"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/cfmeyers/confluence_tool",
    version="0.1.0",
    zip_safe=False,
)
