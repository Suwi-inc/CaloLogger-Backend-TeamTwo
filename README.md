# CaloLogger Backend

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://docs.python.org/3/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![OpenAPI](https://img.shields.io/badge/openapi-6BA539?style=for-the-badge&logo=openapi-initiative&logoColor=fff)](https://www.openapis.org/)
[![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)](https://swagger.io/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://black.readthedocs.io/en/stable/)
[![Typed with: pydantic](https://img.shields.io/badge/typed%20with-pydantic-BA600F.svg?style=for-the-badge)](https://docs.pydantic.dev/)

## Description

Backend for a web-app tracking calories and weight for users.

## Installation

- Install all the project dependency using Poetry

  ```sh
  $ poetry install
  ```
  
- Create `.env` by copying `.env.test` and specifying values

- Run the application from command prompt:

  ```sh
  $ poetry run uvicorn app.main:app --reload
  ```

- Open `localhost:8000/docs` for API Documentation

## Testing

For Testing,

- Run the following command to initiate test:
  ```sh
  $ poetry run pytest
  ```
- To include Coverage Reporting as well:
  ```sh
  $ poetry run pytest --cov-report xml --cov app/
  ```

## License

&copy; MIT License
