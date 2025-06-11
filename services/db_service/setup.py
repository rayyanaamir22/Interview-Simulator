from setuptools import setup, find_packages

setup(
    name="db_service",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.8.0",
        "sqlalchemy>=1.4.23",
        "psycopg2-binary>=2.9.1",
        "python-dotenv>=0.19.0",
    ],
    python_requires=">=3.8",
    author="Interview Simulator Team",
    description="Database Service for Interview Simulator",
    keywords="interview, simulator, database",
) 