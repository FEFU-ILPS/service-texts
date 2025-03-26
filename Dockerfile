FROM python:3.13-slim

# Установка curl для heath-check
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN pip install poetry && poetry config virtualenvs.create false

WORKDIR /service

COPY ./pyproject.toml .

RUN poetry install --only main --no-interaction --no-ansi --no-root

COPY ./alembic.ini .

COPY . .

EXPOSE 8063

CMD ["sh", "-c", "alembic upgrade head && python start.py"]