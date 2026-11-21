# AGENTS.md

Инструкции для ИИ-агентов и разработчиков, работающих с этим репозиторием.

## Что это

Небольшой Flask-пульт для Windows с двумя действиями: выключить и перезагрузить ПК

## Запуск

```bat
start.cmd
```

Скрипт переходит в папку проекта и запускает `main.pyw` через `venv\Scripts\pythonw.exe`, без консоли. При отсутствии venv используется системный `pythonw`.

```bat
python -m venv venv
venv\Scripts\pip install -r requirements.txt
```

Сервер слушает `0.0.0.0:5000`. Открывать как `http://<ip вашего ПК>:5000`.

## Структура

| Файл | Роль |
|---|---|
| `main.pyw` | Flask-приложение, HTML-шаблон и маршруты |
| `start.cmd` | Бесконсольный запуск |
| `requirements.txt` | Зависимости (только Flask) |
| `README.md` | Описание для пользователя |
| `AGENTS.md` | Этот файл |

## Правила

- **Windows only.** Код использует `shutdown.exe` — не пытайся сделать кроссплатформенным без запроса.
- **Не добавляй зависимости без необходимости.** Сейчас нужна только Flask, `requirements.txt` должен оставаться минимальным.
- **Не удаляй файлы без явного разрешения пользователя.**
- **Не трогай системные файлы** и не меняй настройки ОС вне диапазона команд `shutdown /s /t 2` и `shutdown /r /t 2`.
- **Оставляй интерфейс на русском.** Тексты кнопок и ответов — русские, комментарии в коде — по-русски.
- **Не добавляй авторизацию «заодно»** — это меняет модель использования. Обсуди сначала.
- **Не вызывай `/shutdown` и `/reboot` при проверке** — это реально выключит или перезагрузит машину. Тестируй только `/` через `app.test_client()`.

## Проверка изменений

```bat
venv\Scripts\python.exe -c "import ast,pathlib; ast.parse(pathlib.Path('main.pyw').read_text(encoding='utf-8')); print('ok')"
```

Проверка главной страницы без запуска сервера:

```bat
venv\Scripts\python.exe -c "import importlib.util,pathlib; p=pathlib.Path('main.pyw'); s=importlib.util.spec_from_file_location('m',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.app.test_client().get('/').status_code)"
```

Ожидаемый результат: `ok` и `200`.

## Остановка сервера

```powershell
Get-NetTCPConnection -LocalPort 5000 -State Listen |
  ForEach-Object { Stop-Process -Id $_.OwningProcess }
```

## Безопасность

Авторизации нет: любой в той же сети может выключить ПК. Не пробрасывай порт 5000 наружу и не публикуй приложение в интернет без защиты.
