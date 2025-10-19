set windows-powershell := true


[group('DEV')]
dev-up:
    docker compose up database -d 
    uv run python -m src

[group('DEV')]
dev-down:
    docker compose down