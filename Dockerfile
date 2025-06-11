FROM python:3.11-slim

WORKDIR /code

# Сначала только зависимости
COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

# Теперь весь код
COPY . .

# Запуск через poetry (лучше оставить внутри контейнера)
CMD ["poetry", "run", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
