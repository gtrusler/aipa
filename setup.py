from setuptools import setup, find_packages

setup(
    name="aipa",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "httpx[http2]",  # Added http2 for async support
        "python-dotenv",
    ],
)
