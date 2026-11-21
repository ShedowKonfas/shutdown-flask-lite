# ⏻ Пульт питания ПК

Минимальная версия пульта на Flask: только **выключение** и **перезагрузка** компьютера. Ветка `shutdown-reboot-only` — без голосового ассистента, клавиатуры и прочего.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)

## 🚀 Запуск

Двойной клик по **`start.cmd`** — сервер поднимется без консоли.

```bat
start.cmd
```

Скрипт сам перейдёт в папку проекта и запустит `main.pyw` через `venv\Scripts\pythonw.exe` (или системный `pythonw`, если venv нет).

Первый запуск на чистой машине:

```bat
python -m venv venv
venv\Scripts\pip install -r requirements.txt
start.cmd
```

## 🌐 Доступ

Сервер слушает `0.0.0.0:5000` — панель открывается с любого устройства в сети:

```
http://127.0.0.1:5000          — с самого ПК
http://192.168.3.76:5000       — из локальной сети
```

## 🗺️ Маршруты

| URL | Действие |
|---|---|
| `/` | панель с двумя кнопками |
| `/shutdown` | `shutdown /s /t 2` |
| `/reboot` | `shutdown /r /t 2` |

## 📁 Структура

```
shutdown-flask/
├── main.pyw          # Flask-приложение и вёрстка
├── start.cmd         # запуск без консоли
├── requirements.txt  # зависимости (Flask)
└── venv/             # виртуальное окружение
```

## 🔒 Безопасность

Авторизации нет: выключить или перезагрузить ПК может любой, кто попадёт в ту же сеть. Не пробрасывайте порт 5000 наружу.

## 🌿 Ветки

- `main` — полная версия с Глашей и удалённой клавиатурой;
- `shutdown-reboot-only` — только питание ПК (эта ветка).
