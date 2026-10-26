# Calculator — простой сервис-калькулятор

Небольшой сервис калькулятор на FastAPI.

**Для кого:** небольшой учебный шаблон для разработчиков.

## Установка

Python 3.10+.

```bash
git clone https://github.com/W1ll1am32/Calculator.git
cd Calculator

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements-dev.txt
```

## Запуск

```bash
uvicorn app_final:app --host 0.0.0.0 --port 8000 --env-file .env

Документация: <http://127.0.0.1:8000/docs>

## Тесты

```bash
python -m pytest -v
```

## Переменные окружения

| Переменная | По умолчанию | Назначение |
|---|---|---|
| `APP_NAME` | `Calculator` | Название сервиса |
| `APP_VERSION` | `1.0.0` | Версия сервиса |
| `PRECISION` | `4` | Сколько знаков после запятой |
| `HISTORY_SIZE` | `10` | Сколько последних вычислений хранить |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

Пример лежит в `.env.example`, для настройки перменных используйте `.env`

## Диагностика

```bash
curl http://127.0.0.1:8000/health
# {"status":"ok"}

curl http://127.0.0.1:8000/version
# {"name": Calculator, "version": "1.0.0"}
```

Логи пишутся в терминал, где запущен `uvicorn`.