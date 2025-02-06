echo "Applying database migrations..."
alembic upgrade head

echo "Starting FastAPI..."
uvicorn src.main:app --host 0.0.0.0 --port 8000