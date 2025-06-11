from setuptools import setup, find_packages

setup(
    name="interaction_service",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.8.0",
        "python-dotenv>=0.19.0",
    ],
    python_requires=">=3.8",
    author="Interview Simulator Team",
    description="Interaction Service for Interview Simulator",
    keywords="interview, simulator, interaction",
) 