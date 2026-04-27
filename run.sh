echo "Starting StyleClone..."

echo "Starting FastAPI backend on port 8000..."
uvicorn src.main:app --reload --port 8000 &
FASTAPI_PID=$!

echo "Starting Telegram Bot..."
python -m src.bot.bot

echo "Stopping FastAPI..."
kill $FASTAPI_PID 2>/dev/null