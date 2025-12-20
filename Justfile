set windows-powershell := true


[group('DEV')]
up-db:
    docker compose up database -d --wait

[group('DEV')]
migrate:
    uv run alembic upgrade head

[group('DEV')]
test-unit:
    pytest tests/unit -v