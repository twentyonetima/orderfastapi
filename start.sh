#!/bin/sh

echo "⏳ Ждем, пока PostgreSQL будет готов..."
/wait-for-it.sh db:5432 --timeout=60 --strict -- echo "✅ PostgreSQL готов"

echo "⏳ Ждем, пока Redis будет готов..."
/wait-for-it.sh redis:6379 --timeout=60 --strict -- echo "✅ Redis готов"

echo "⏳ Ждем, пока RabbitMQ будет готов..."
/wait-for-it.sh rabbitmq:5672 --timeout=60 --strict -- echo "✅ RabbitMQ готов"

echo "✅ Все сервисы готовы, запускаем миграции Alembic..."
alembic upgrade head

echo "🚀 Запускаем FastAPI сервер..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload