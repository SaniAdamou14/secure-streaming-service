#!/bin/bash
set -e

echo "=== Environment ==="
python --version
git --version

echo ""
echo "=== Ruff Format Check ==="
ruff format --check .

echo ""
echo "=== Ruff Lint ==="
ruff check .

echo ""
echo "=== Pytest ==="
pytest -q --cov=app --cov-report=term-missing --cov-report=html

echo ""
echo "=== Bandit ==="
bandit -r app

echo ""
echo "=== Gitleaks ==="
gitleaks detect -s . --no-banner

echo ""
echo "=== Docker Build ==="
docker build -t secure-streaming-service .

echo ""
echo "=== All checks passed ==="
