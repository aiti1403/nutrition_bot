# Бот для опроса о питании

Телеграм-бот для проведения опросов о пищевом поведении и эмоциональном состоянии пользователей.

## Описание

Этот бот помогает пользователям отслеживать свое эмоциональное состояние и пищевое поведение через серию вопросов. После завершения опроса бот предоставляет персонализированные рекомендации на основе ответов пользователя.

## Функциональность

- Проведение опроса из 16 вопросов
- Сохранение ответов пользователей в базе данных
- Предоставление персонализированных рекомендаций
- Административная панель для просмотра и экспорта результатов

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/aiti1403/nutrition_bot
cd nutrition_bot
```

2. Установите необходимые зависимости:
```bash
pip install aiogram aiosqlite
```

3. Отредактируйте файл main.py, добавив в него токен вашего бота:
```python
BOT_TOKEN = "ваш_токен_бота"
```

4. Запустите бота:
```bash
python main.py
```

## Использование

### Пользователи
1. Начните диалог с ботом в Telegram
2. Используйте команду `/start` для начала взаимодействия
3. Используйте команду `/survey` для начала опроса
4. Отвечайте на вопросы, следуя инструкциям бота

### Администраторы
1. Используйте команду `/admin` для доступа к административной панели
2. Введите пароль администратора (по умолчанию: "admin123")
3. Используйте доступные функции:
   - Просмотр результатов опросов
   - Экспорт данных в CSV-формат

## Разработка

### Добавление новых вопросов
1. Создайте новую клавиатуру в `keyboards/survey_kb.py`
2. Добавьте обработчик для нового вопроса в `handlers/survey.py`

### Изменение рекомендаций
Рекомендации формируются в обработчике последнего вопроса в файле `handlers/survey.py`. Для изменения рекомендаций отредактируйте соответствующий блок кода.

## Лицензия

Этот проект распространяется под лицензией MIT. См. файл LICENSE для получения дополнительной информации.
