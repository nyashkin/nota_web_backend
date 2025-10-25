FROM python:3.13-alpine

WORKDIR /app

# ADD UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ./uv.lock ./pyproject.toml ./

RUN uv sync --no-dev

COPY . .

CMD ["sh", "-c", "uv run --no-dev alembic upgrade head && uv run --no-dev python -m src"]