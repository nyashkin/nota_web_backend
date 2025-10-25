set windows-powershell := true


[group('DEV')]
dev-up:
    docker compose up database -d 
    uv run python -m src

[group('DEV')]
up-db:
    docker compose up database -d

[group('DEV')]
dev-down:
    docker compose down

[group('DEV')]
test:
    pytest -v