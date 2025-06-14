# 🧠 Friends LLM Chat

Мультимодальный веб-чат с персонажами из сериала **«Друзья»**, основанный на LLM (Gemma 3 12B) и FastAPI.

## 🚀 Возможности

- 🌐 Веб-интерфейс с выбором персонажа и полем ввода
- 🤖 Подключение к локальной LLM через Cloudflare Tunnel
- 💬 Ведение диалогов с запоминанием истории
- 🗃 Хранение истории сообщений в базе данных (SQLite)
- 📜 Интерфейс просмотра истории по каждой сессии
- 🐳 Docker + Docker Compose для удобного развёртывания

---

## 🖼️ Интерфейс

- Главная страница: `http://<IP>:8000/`
- Просмотр истории: `http://<IP>:8000/history_ui/{session_id}`

---

## 🛠️ Архитектура

- **FastAPI** — веб-сервер и API
- **Jinja2** — HTML-шаблоны
- **Gemma 3 12B** — LLM через LM Studio
- **Cloudflare Tunnel** — безопасный публичный доступ к localhost
- **SQLite** — база данных
- **Docker** — контейнеризация и запуск

---

## 🧩 Пример `.env`

```env
LM_STUDIO_URL=https://lm.otus-test-1234.online
DEFAULT_CHARACTER=phoebe
````

---

## 📦 Как развернуть

### 1. Установи зависимости

```bash
poetry install
```

### 2. Подними Docker (приложение)

```bash
docker compose up --build
```

### 3. Запусти Cloudflare Tunnel (на локальной машине с LM Studio)

```bash
cloudflared tunnel run otus_example
```

---

## 📊 Структура БД

* `ChatSession` — ID, персонаж, дата
* `Message` — роль (user/bot), текст, дата

---

## 🧪 Тестирование

```bash
make test
# или
poetry run pytest
```

---

## 📌 Идеи для развития

* 🎤 Голос персонажей (TTS)
* 🧠 Память на уровне нескольких сообщений
* 📊 Админка: статистика по диалогам
* 🤖 Telegram-бот
* 📷 Интеграция с генерацией изображений по сценам

