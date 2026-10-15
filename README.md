# Architecture-Decision-Records-ADR-
Описание: система управления архитектурными решениями 1С-проекта. ADR, RFC, диаграммы, поиск, экспорт.


Система управления архитектурными решениями 1С-проекта.

## Возможности
- ADR: 5 статусов, Markdown-формат, метаданные
- RFC: предложения с impact/timeline
- Registry: создание, поиск, статистика
- Поиск по ADR (TF-IDF)
- Экспорт в Markdown, JSON, HTML
- REST API

## Запуск
```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
pytest -v
```
