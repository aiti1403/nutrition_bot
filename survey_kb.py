from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

# Клавиатуры для каждого вопроса
def get_question_1_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Сильно"),
        KeyboardButton(text="Средне"),
        KeyboardButton(text="Не очень"),
        KeyboardButton(text="Не пойму")
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_question_2_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Более 3 часов назад"),
        KeyboardButton(text="От 1 до 3 часов назад"),
        KeyboardButton(text="Недавно (в течении часа)")
    )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_question_3_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Очень плохо"),
        KeyboardButton(text="Плохо"),
        KeyboardButton(text="Средне"),
        KeyboardButton(text="Хорошо"),
        KeyboardButton(text="Прекрасно")
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_question_4_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Да"),
        KeyboardButton(text="Нет")
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_question_5_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Грусть", callback_data="emotion_sadness"),
        InlineKeyboardButton(text="Наслаждение", callback_data="emotion_pleasure"),
        InlineKeyboardButton(text="Страх", callback_data="emotion_fear"),
        InlineKeyboardButton(text="Злость", callback_data="emotion_anger"),
        InlineKeyboardButton(text="Удивление", callback_data="emotion_surprise"),
        InlineKeyboardButton(text="Отвращение", callback_data="emotion_disgust"),
        InlineKeyboardButton(text="Другое (вписать)", callback_data="emotion_other")
    )
    builder.add(InlineKeyboardButton(text="✅ Подтвердить", callback_data="emotion_confirm"))
    builder.adjust(2)
    return builder.as_markup()

def get_question_6_kb():
    builder = ReplyKeyboardBuilder()
    for i in range(1, 11):
        builder.add(KeyboardButton(text=str(i)))
    builder.adjust(5)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_question_7_kb():
    return get_question_4_kb()

def get_question_8_kb():
    builder = InlineKeyboardBuilder()
    options = [
        ("Конкретное блюдо", "food_specific"),
        ("Сладкое", "food_sweet"),
        ("Соленое", "food_salty"),
        ("Кислое", "food_sour"),
        ("Теплое", "food_warm"),
        ("Холодное", "food_cold"),
        ("Хрустящее", "food_crispy"),
        ("Нежное", "food_tender"),
        ("Острое", "food_spicy"),
        ("Сытное", "food_filling"),
        ("Легкое", "food_light"),
        ("Не знаю", "food_dontknow"),
        ("Другое (вписать)", "food_other")
    ]
    
    for text, callback_data in options:
        builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    
    builder.add(InlineKeyboardButton(text="✅ Подтвердить", callback_data="food_confirm"))
    builder.adjust(2)
    return builder.as_markup()

def get_question_9_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Готова"),
        KeyboardButton(text="Не знаю"),
        KeyboardButton(text="Совсем не готова")
    )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_question_10_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Да"),
        KeyboardButton(text="Нет"),
        KeyboardButton(text="Не знаю")
    )
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_question_11_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Я ненавижу себя"),
        KeyboardButton(text="Я разочарована собой"),
        KeyboardButton(text="Я немного недовольна собой"),
        KeyboardButton(text="Я довольна собой"),
        KeyboardButton(text="Я горжусь собой")
    )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_question_12_kb():
    builder = InlineKeyboardBuilder()
    options = [
        ("Отдыха", "need_rest"),
        ("Человека рядом", "need_person"),
        ("Спокойствия", "need_calm"),
        ("Уединения", "need_solitude"),
        ("Любви", "need_listener"),
        ("Заботы", "need_care"),
        ("Другое (вписать)", "need_other")
    ]
    
    for text, callback_data in options:
        builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    
    builder.add(InlineKeyboardButton(text="✅ Подтвердить", callback_data="need_confirm"))
    builder.adjust(2)
    return builder.as_markup()

def get_question_13_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Да"),
        KeyboardButton(text="Нет"),
        KeyboardButton(text="Не уверена")
    )
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_question_14_kb():
    return get_question_4_kb()

def get_question_15_kb():
    builder = InlineKeyboardBuilder()
    options = [
        ("Сон", "help_sleep"),
        ("Прогулка", "help_walk"),
        ("Ванная", "help_bath"),
        ("Попить воды", "help_water"),
        ("Чай", "help_tea"),
        ("Массаж", "help_massage"),
        ("Уход за собой", "help_selfcare"),
        ("Фильм или сериал", "help_movie"),
        ("Выговориться", "help_vent"),
        ("Поплакать", "help_cry"),
        ("Написать свои эмоции", "help_write"),
        ("Другое", "help_other")
    ]
    
    for text, callback_data in options:
        builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    
    builder.add(InlineKeyboardButton(text="✅ Подтвердить", callback_data="help_confirm"))
    builder.adjust(2)
    return builder.as_markup()

def get_question_16_kb():
    return get_question_10_kb()

# Клавиатура для админа
def get_admin_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Просмотр результатов"),
        KeyboardButton(text="Экспорт данных"),
        KeyboardButton(text="Выход из админки")
    )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

# Клавиатура для оплаты
def get_payment_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Оплатить", callback_data="pay"),
        InlineKeyboardButton(text="Отмена", callback_data="cancel_payment")
    )
    builder.adjust(1)
    return builder.as_markup()

