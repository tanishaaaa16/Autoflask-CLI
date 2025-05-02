from setuptools import setup, find_packages

setup(
    name="autoflask-cli",
    version="1.0.0",
    description="A CLI tool for automating Flask app creation and management",
    author="Tanisha Singh",
    author_email="your.email@example.com",
    packages=find_packages(),
    py_modules=["autoflask"],
    install_requires=[
        "flask",  # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "autoflask=autoflask:main",  # Replace 'main' with the entry function in autoflask.py
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)