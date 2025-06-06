from setuptools import setup, find_packages

setup(
    name="interview-interaction-service",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-cloud-speech>=2.21.0",
        "google-cloud-texttospeech>=2.14.1",
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "deepface>=0.0.79",
        "numpy>=1.24.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
        "python-multipart>=0.0.6",
        "websockets>=11.0.3",
    ],
    author="Interview Simulator Team",
    description="Interview interaction service for the Interview Simulator project",
    python_requires=">=3.8",
) 