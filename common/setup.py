from setuptools import setup, find_packages

with open("../README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="datatoolkit-common",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Common utilities for data engineering tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/data-toolkit",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
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
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=1.10.0",
        "python-dateutil>=2.8.0",
        "PyYAML>=6.0",
        "requests>=2.28.0",
    ],
)