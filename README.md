# 🏐 Volley Analytics

Веб-система для автоматического анализа волейбольных видео: находит розыгрыши, определяет время начала и окончания, распознаёт сторону подачи.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![SQLite](https://img.shields.io/badge/SQLite-database-003B57)
![Celery](https://img.shields.io/badge/Celery-worker-37814A)
![Redis](https://img.shields.io/badge/Redis-queue-DC382D)

---

## О проекте

Система принимает на вход волейбольное видео, автоматически находит на нём игровые эпизоды (розыгрыши) и показывает список: когда начался розыгрыш, когда закончился и кто подавал.

Исходные данные — одна запись волейбольного матча длительностью около 21 минуты.

---

## Архитектура
Пользователь
│
▼
React (браузер) ──▶ FastAPI (backend) ──▶ SQLite (база данных)
│
▼
Redis (очередь)
│
▼
Celery (worker) ──▶ YOLO + трекер
│
▼
Файлы (видео и результаты)

## 🛠️ Технологии

| Слой | Технология |
|---|---|
| Frontend | React |
| Backend | FastAPI |
| ORM | SQLAlchemy |
| Миграции | Alembic |
| База данных | SQLite |
| Очередь | Redis |
| Workers | Celery |
| ML | YOLO + fast-volleyball-tracking |
| Запуск | Docker Compose |

## Структура проекта
---
Volleyball/
├── app/                  # код приложения
│   ├── database.py       # подключение к базе данных
│   ├── models.py         # модели SQLAlchemy
│   ├── main.py           # FastAPI
│   └── workers/          # Celery-задачи
├── alembic/              # миграции
│   └── versions/         # файлы миграций
├── data/                 # данные
│   ├── uploads/          # загруженные видео
│   ├── artifacts/        # результаты работы нейросети
│   └── app.db            # база данных SQLite
├── docs/                 # документация
│   ├── architecture.md   # описание архитектуры
│   └── er_diagram.png    # ER-диаграмма
├── requirements.txt      # зависимости
└── README.md             # этот файл

