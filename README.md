# Чат-бот опросник "Самооценка"

* Ответь на 15 вопросов и 4 варианта ответа.

* Будьте максимально честны с собой.

* Узнай свой уровень самооценки

## Переменные окружения

1. Токен Вашего чат-бота

```bash
BOT_TOKEN='YOUR_BOT_TOKEN'
```

2. Для получения логов в Телеграм

```bash
LOGGING_IDS=telegram_id,telegram_id
```

## Запустить dev-версию

Установите переменную окружения

```bash
DEV=True
```

```bash
python bot.py
```

## Запуск prod на сервере

1. Установите переменные

```bash
HOST=https://example.com
PORT=YOUR_PORT (default=5001)
```

2. Добавьте в config nginx реверс-прокси и location

```bash
location /BOT_TOKEN {
    include '/etc/nginx/proxy_params';
    proxy_pass http://127.0.0.1:PORT/BOT_TOKEN/;
}
```


## Цель проекта

Часть проекта чат-бота центра нестандартной психологии "Сомагенез".
