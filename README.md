# paputapp

A small local web app for demonstrating automated UI and REST API testing.

## Stack

- FastAPI + Jinja2 (UI, port 8001)
- FastAPI + SQLAlchemy (API, port 8000)
- SQLite database
- pytest + Selenium + Allure for tests

## Running the app

```
uvicorn src.main:app --port 8001 --reload --reload-dir src
```

## Running tests

```
pytest --log-cli-level=INFO .\tests\test_main.py
```
