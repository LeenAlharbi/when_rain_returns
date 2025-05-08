# setup.py
from pathlib import Path
from setuptools import setup, find_packages
import os

def read_long_description():
    with open(Path(__file__).with_name("README.md"), encoding="utf-8") as f:
        return f.read()

setup(
    name="when_rain_returns",
    version="0.1.0",
    author="name",
    author_email="name@example.com",
    description="Tools for cleaning, analysing, and forecasting Saudi rainfall data",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/<user>/when_rain_returns",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scikit-learn",
        "jupyter"
    ],
    include_package_data=True,
    package_data={"": ["data/raw/*", "data/cleaned/*"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ],
    python_requires=">=3.9",
entry_points={
    "console_scripts": [
        "run-my-project=when_rain_returns.main:main",   
    ],
},
)