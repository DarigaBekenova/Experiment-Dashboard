# Experiment Dashboard — Анализ данных

Дашборд результатов ML-экспериментов для исследования по анализу данных.

## Связь с диссертацией
Приложение решает задачу учёта и сравнения экспериментов: датасет, модель, статус, accuracy, длительность. Пользователь — исследователь. Данные — синтетические, открытые.

## Быстрый старт
```bash
cp .env.example .env
docker compose up --build
```
- Фронтенд: http://localhost:3000
- API docs: http://localhost:8000/docs

## Локальная разработка
Бэкенд:
```bash
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```
Фронтенд:
```bash
cd frontend
npm install
npm run dev
```

## Тесты
```bash
cd backend
uv run pytest -q
uv run ruff check .
```

## Структура
- `backend/app/modules/experiments/` — models / schemas / service / router
- `frontend/src/app/experiments/` — список, карточка, формы
- `docs/architecture.md` — архитектура

## Данные
Seed: `docker compose exec backend python -m scripts.seed` — 24 синтетических эксперимента.

## AI assistance
При разработке использовался ИИ-ассистент: генерация CRUD, тестов, фронтенда по методичке; проверки выполнены запуском pytest и ruff.

## Лицензия
MIT
