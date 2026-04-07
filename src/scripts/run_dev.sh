#!/usr/bin/env bash
set -euo pipefail
export UV_CACHE_DIR="${UV_CACHE_DIR:-/home/z/.cache/uv}"
cp .env.example .env 2>/dev/null || true
exec uv run python -m bot