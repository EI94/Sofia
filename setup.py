from setuptools import setup, find_packages

setup(
    name="sofia-lite",
    version="1.0.0",
    description="Sofia AI Lite - Minimal core package",
    author="Sofia AI Team",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.116.1",
        "uvicorn==0.35.0",
        "openai==1.97.0",
        "twilio==9.6.5",
        "google-cloud-firestore==2.21.0",
        "python-multipart==0.0.20",
        "fasttext==0.9.2",
        "psutil==6.1.0",
        "aiohttp==3.10.11",
        "PyYAML==6.0.1",
    ],
    python_requires=">=3.8",
) 