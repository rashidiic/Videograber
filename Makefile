.PHONY: run test lint typecheck format clean docker-build docker-up docker-down docker-logs

run:
        UV_CACHE_DIR=/home/z/.cache/uv uv run python -m bot

test:
        UV_CACHE_DIR=/home/z/.cache/uv uv run pytest tests/ -v

lint:
        UV_CACHE_DIR=/home/z/.cache/uv uv run ruff check src/ tests/

typecheck:
        UV_CACHE_DIR=/home/z/.cache/uv uv run mypy src/

format:
        UV_CACHE_DIR=/home/z/.cache/uv uv run ruff format src/ tests/

clean:
        find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
        rm -rf .mypy_cache .ruff_cache

docker-build:
        docker compose build

docker-up:
        docker compose up -d --build

docker-down:
        docker compose down

docker-logs:
        docker compose logs -f bot