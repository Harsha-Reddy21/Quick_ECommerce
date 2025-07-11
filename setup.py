from setuptools import setup, find_packages

setup(
    name="quick-ecommerce",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.23.2",
        "sqlalchemy==2.0.23",
        "psycopg2-binary==2.9.9",
        "pydantic==2.4.2",
        "python-jose==3.3.0",
        "passlib==1.7.4",
        "python-multipart==0.0.6",
        "bcrypt==4.0.1",
        "alembic==1.12.1",
        "python-dotenv==1.0.0",
        "pillow==10.1.0",
        "email-validator==2.0.0",
        "starlette==0.27.0",
        "typing-extensions==4.8.0",
        "cryptography==41.0.5",
    ],
    python_requires=">=3.8",
) 