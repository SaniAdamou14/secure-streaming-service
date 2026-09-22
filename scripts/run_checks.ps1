Write-Host "=== Environment ===" -ForegroundColor Cyan
python --version
git --version

Write-Host "`n=== Ruff Format Check ===" -ForegroundColor Cyan
ruff format --check .

Write-Host "`n=== Ruff Lint ===" -ForegroundColor Cyan
ruff check .

Write-Host "`n=== Pytest ===" -ForegroundColor Cyan
pytest -q --cov=app --cov-report=term-missing --cov-report=html

Write-Host "`n=== Bandit ===" -ForegroundColor Cyan
bandit -r app

Write-Host "`n=== Gitleaks ===" -ForegroundColor Cyan
gitleaks detect -s . --no-banner

Write-Host "`n=== Docker Build ===" -ForegroundColor Cyan
docker build -t secure-streaming-service .

Write-Host "`n=== All checks passed ===" -ForegroundColor Green
