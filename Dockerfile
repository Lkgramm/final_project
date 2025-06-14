FROM python:3.11-slim

WORKDIR /code

COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

RUN apt update && apt install curl -y

COPY src/ ./src/
COPY src/app/templates/ ./templates/

ENV PYTHONPATH=/code/src

CMD ["poetry", "run", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
