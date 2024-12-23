from setuptools import setup, find_packages

setup(
    name="lock",
    version="1.0.0",
    description="License Optimization and Control Kit",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/bailey13x/LOCK",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "cryptography",
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
