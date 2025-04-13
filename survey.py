from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.states import SurveyStates
from keyboards.survey_kb import (
    get_question_1_kb, get_question_2_kb, get_question_3_kb, get_question_4_kb,
    get_question_5_kb, get_question_6_kb, get_question_7_kb, get_question_8_kb,
    get_question_9_kb, get_question_10_kb, get_question_11_kb, get_question_12_kb,
    get_question_13_kb, get_question_14_kb, get_question_15_kb, get_question_16_kb
)
from database.database import save_answer, save_completed_survey

router = Router()

# Обработчики для каждого вопроса
@router.message(SurveyStates.question_1)
async def process_question_1(message: Message, state: FSMContext):
    # Сохраняем ответ на первый вопрос
    await save_answer(message.from_user.id, 1, message.text)
    
    # Обновляем данные состояния
    await state.update_data(answers={1: message.text})
    
    # Задаем второй вопрос
    await message.answer(
        "Вопрос 2: Как давно ты ел(а)?",
        reply_markup=get_question_2_kb()
    )
    
    # Переходим к следующему состоянию
    await state.set_state(SurveyStates.question_2)

@router.message(SurveyStates.question_2)
async def process_question_2(message: Message, state: FSMContext):
    # Сохраняем ответ на второй вопрос
    await save_answer(message.from_user.id, 2, message.text)
    
    # Получаем предыдущие ответы и добавляем новый
    data = await state.get_data()
    answers = data.get("answers", {})
    answers[2] = message.text
    await state.update_data(answers=answers)
    
    # Задаем третий вопрос
    await message.answer(
        "Вопрос 3: Как ты сейчас себя чувствуешь?",
        reply_markup=get_question_3_kb()
    )
    
    # Переходим к следующему состоянию
    await state.set_state(SurveyStates.question_3)

@router.message(SurveyStates.question_3)
async def process_question_3(message: Message, state: FSMContext):
    await save_answer(message.from_user.id, 3, message.text)
    
    data = await state.get_data()
    answers = data.get("answers", {})
    answers[3] = message.text
    await state.update_data(answers=answers)
    
    await message.answer(
        "Вопрос 4: Что-то тебя сильно расстроило в последний час?",
        reply_markup=get_question_4_kb()
    )
    
    await state.set_state(SurveyStates.question_4)

@router.message(SurveyStates.question_4)
async def process_question_4(message: Message, state: FSMContext):
    await save_answer(message.from_user.id, 4, message.text)
    
    data = await state.get_data()
    answers = data.get("answers", {})
    answers[4] = message.text
    await state.update_data(answers=answers)
    
    await message.answer(
        "Вопрос 5: Какая основная эмоция? (можно выбрать несколько)",
        reply_markup=get_question_5_kb()
    )
    
    # Инициализируем список для хранения выбранных эмоций
    await state.update_data(selected_emotions=[])
    
    await state.set_state(SurveyStates.question_5)

# Обработчик для множественного выбора эмоций
@router.callback_query(F.data.startswith("emotion_"), SurveyStates.question_5)
async def process_emotion_selection(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_emotions = data.get("selected_emotions", [])
    
    if callback.data == "emotion_confirm":
        if not selected_emotions:
            await callback.answer("Пожалуйста, выберите хотя бы одну эмоцию")
            return
        
        # Сохраняем выбранные эмоции
        emotions_str = ", ".join(selected_emotions)
        await save_answer(callback.from_user.id, 5, emotions_str)
        
        answers = data.get("answers", {})
        answers[5] = emotions_str
        await state.update_data(answers=answers)

        await callback.message.answer(f"Вы выбрали: {emotions_str}")
        
        await callback.message.answer(
            "Вопрос 6: Насколько сильна эта эмоция? (от 1 до 10)",
            reply_markup=get_question_6_kb()
        )
        
        await state.set_state(SurveyStates.question_6)
    elif callback.data == "emotion_other":
        await callback.message.answer("Пожалуйста, напишите, какая эмоция у вас сейчас:")
        await state.set_state(SurveyStates.custom_answer)
        await state.update_data(custom_field="emotion")
    else:
        emotion = callback.data.replace("emotion_", "")
        
        # Преобразуем технические названия в читаемые
        emotion_names = {
            "sadness": "Грусть",
            "pleasure": "Наслаждение",
            "fear": "Страх",
            "anger": "Злость",
            "surprise": "Удивление",
            "disgust": "Отвращение"
        }
        
        readable_emotion = emotion_names.get(emotion, emotion)
        
        if readable_emotion in selected_emotions:
            selected_emotions.remove(readable_emotion)
            await callback.answer(f"Удалено: {readable_emotion}")
        else:
            selected_emotions.append(readable_emotion)
            await callback.answer(f"Добавлено: {readable_emotion}")
        
        await state.update_data(selected_emotions=selected_emotions)
    
    await callback.answer()

# Обработчик для пользовательских ответов
@router.message(SurveyStates.custom_answer)
async def process_custom_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    custom_field = data.get("custom_field")
    
    if custom_field == "emotion":
        selected_emotions = data.get("selected_emotions", [])
        selected_emotions.append(f"Другое: {message.text}")
        await state.update_data(selected_emotions=selected_emotions)
        
        await message.answer(
            "Эмоция добавлена. Выберите другие эмоции или нажмите 'Подтвердить выбор'",
            reply_markup=get_question_5_kb()
        )
        
        await state.set_state(SurveyStates.question_5)
    elif custom_field == "food":
        selected_foods = data.get("selected_foods", [])
        selected_foods.append(f"Другое: {message.text}")
        await state.update_data(selected_foods=selected_foods)
        
        await message.answer(
            "Предпочтение добавлено. Выберите другие варианты или нажмите 'Подтвердить выбор'",
            reply_markup=get_question_8_kb()
        )
        
        await state.set_state(SurveyStates.question_8)
    elif custom_field == "need":
        selected_needs = data.get("selected_needs", [])
        selected_needs.append(f"Другое: {message.text}")
        await state.update_data(selected_needs=selected_needs)
        
        await message.answer(
            "Потребность добавлена. Выберите другие варианты или нажмите 'Подтвердить выбор'",
            reply_markup=get_question_12_kb()
        )
        
        await state.set_state(SurveyStates.question_12)
    elif custom_field == "help":
        selected_helps = data.get("selected_helps", [])
        selected_helps.append(f"Другое: {message.text}")
        await state.update_data(selected_helps=selected_helps)
        
        await message.answer(
            "Вариант добавлен. Выберите другие варианты или нажмите 'Подтвердить выбор'",
            reply_markup=get_question_15_kb()
        )
        
        await state.set_state(SurveyStates.question_15)

@router.message(SurveyStates.question_6)
async def process_question_6(message: Message, state: FSMContext):
    # Проверяем, что ответ - число от 1 до 10
    if not message.text.isdigit() or int(message.text) < 1 or int(message.text) > 10:
        await message.answer("Пожалуйста, введите число от 1 до 10")
        return
    
    await save_answer(message.from_user.id, 6, message.text)
    
    data = await state.get_data()
    answers = data.get("answers", {})
    answers[6] = message.text
    await state.update_data(answers=answers)
    
    await message.answer(
        "Вопрос 7: Понимаешь ли ты, что именно сейчас хочешь съесть?",
        reply_markup=get_question_7_kb()
    )
    
    await state.set_state(SurveyStates.question_7)

@router.message(SurveyStates.question_7)
async def process_question_7(message: Message, state: FSMContext):
    await save_answer(message.from_user.id, 7, message.text)
    
    data = await state.get_data()
    answers = data.get("answers", {})
    answers[7] = message.text
    await state.update_data(answers=answers)
    
    await message.answer(
        "Вопрос 8: Что ты хочешь поесть? (можно выбрать несколько)",
        reply_markup=get_question_8_kb()
    )
    
    # Инициализируем список для хранения выбранных предпочтений
    await state.update_data(selected_foods=[])
    
    await state.set_state(SurveyStates.question_8)

@router.callback_query(F.data.startswith("food_"), SurveyStates.question_8)
async def process_food_selection(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_foods = data.get("selected_foods", [])
    
    if callback.data == "food_confirm":
        if not selected_foods:
            await callback.answer("Пожалуйста, выберите хотя бы один вариант")
            return
        
        # Сохраняем выбранные предпочтения
        foods_str = ", ".join(selected_foods)
        await save_answer(callback.from_user.id, 8, foods_str)
        
        answers = data.get("answers", {})
        answers[8] = foods_str
        await state.update_data(answers=answers)

        await callback.message.answer(f"Вы выбрали: {foods_str}")
        
        await callback.message.answer(
            "Вопрос 9: Насколько ты готов(а) отслеживать свое насыщение?",
            reply_markup=get_question_9_kb()
        )
        
        await state.set_state(SurveyStates.question_9)
    elif callback.data == "food_other":
        await callback.message.answer("Пожалуйста, напишите, что вы хотите поесть:")
        await state.set_state(SurveyStates.custom_answer)
        await state.update_data(custom_field="food")
    else:
        food = callback.data.replace("food_", "")
        
        # Преобразуем технические названия в читаемые
        food_names = {
            "specific": "Конкретное блюдо",
            "sweet": "Сладкое",
            "salty": "Соленое",
            "sour": "Кислое",
            "warm": "Теплое",
            "cold": "Холодное",
            "crispy": "Хрустящее",
            "tender": "Нежное",
            "spicy": "Острое",
            "filling": "Сытное",
            "light": "Легкое",
            "dontknow": "Не знаю"
        }
        
        readable_food = food_names.get(food, food)
        
        if readable_food in selected_foods:
            selected_foods.remove(readable_food)
            await callback.answer(f"Удалено: {readable_food}")
        else:
            selected_foods.append(readable_food)
            await callback.answer(f"Добавлено: {readable_food}")
        
        await state.update_data(selected_foods=selected_foods)
    
    await callback.answer()

@router.message(SurveyStates.question_9)
async def process_question_9(message: Message, state: FSMContext):
    await save_answer(message.from_user.id, 9, message.text)
    
    data = await state.get_data()
    answers = data.get("answers", {})
    answers[9] = message.text
    await state.update_data(answers=answers)
    
    await message.answer(
        "Вопрос 10: Будешь ли ты винить себя за то, что сейчас поел(а)?",
        reply_markup=get_question_10_kb()
    )
    
    await state.set_state(SurveyStates.question_10)

@router.message(SurveyStates.question_10)
async def process_question_10(message: Message, state: FSMContext):
    await save_answer(message.from_user.id, 10, message.text)
    
    data = await state.get_data()
    answers = data.get("answers", {})
    answers[10] = message.text
    await state.update_data(answers=answers)
    
    await message.answer(
        "Вопрос 11: Как ты сейчас к себе относишься?",
        reply_markup=get_question_11_kb()
    )
    
    await state.set_state(SurveyStates.question_11)

@router.message(SurveyStates.question_11)
async def process_question_11(message: Message, state: FSMContext):
    await save_answer(message.from_user.id, 11, message.text)
    
    data = await state.get_data()
    answers = data.get("answers", {})
    answers[11] = message.text
    await state.update_data(answers=answers)
    
    await message.answer(
        "Вопрос 12: Чего сейчас тебе не хватает? (можно выбрать несколько)",
        reply_markup=get_question_12_kb()
    )
    
    # Инициализируем список для хранения выбранных потребностей
    await state.update_data(selected_needs=[])
    
    await state.set_state(SurveyStates.question_12)

@router.callback_query(F.data.startswith("need_"), SurveyStates.question_12)
async def process_need_selection(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_needs = data.get("selected_needs", [])
    
    if callback.data == "need_confirm":
        if not selected_needs:
            await callback.answer("Пожалуйста, выберите хотя бы один вариант")
            return
        
        # Сохраняем выбранные потребности
        needs_str = ", ".join(selected_needs)
        await save_answer(callback.from_user.id, 12, needs_str)
        
        answers = data.get("answers", {})
        answers[12] = needs_str
        await state.update_data(answers=answers)

        await callback.message.answer(f"Вы выбрали: {needs_str}")
        
        await callback.message.answer(
            "Вопрос 13: Есть ли в тебе силы поработать со своими эмоциями?",
            reply_markup=get_question_13_kb()
        )
        
        await state.set_state(SurveyStates.question_13)
    elif callback.data == "need_other":
        await callback.message.answer("Пожалуйста, напишите, чего вам не хватает:")
        await state.set_state(SurveyStates.custom_answer)
        await state.update_data(custom_field="need")
    else:
        need = callback.data.replace("need_", "")
        
        # Преобразуем технические названия в читаемые
        need_names = {
            "rest": "Отдыха",
            "person": "Человека рядом",
            "calm": "Спокойствия",
            "solitude": "Уединения",
            "listener": "Любви",
            "care": "Заботы"
        }
        
        readable_need = need_names.get(need, need)
        
        if readable_need in selected_needs:
            selected_needs.remove(readable_need)
            await callback.answer(f"Удалено: {readable_need}")
        else:
            selected_needs.append(readable_need)
            await callback.answer(f"Добавлено: {readable_need}")
        
        await state.update_data(selected_needs=selected_needs)
    
    await callback.answer()

@router.message(SurveyStates.question_13)
async def process_question_13(message: Message, state: FSMContext):
    await save_answer(message.from_user.id, 13, message.text)
    
    data = await state.get_data()
    answers = data.get("answers", {})
    answers[13] = message.text
    await state.update_data(answers=answers)
    
    await message.answer(
        "Вопрос 14: Есть ли тот, кто готов тебя выслушать сейчас?",
        reply_markup=get_question_14_kb()
    )
    
    await state.set_state(SurveyStates.question_14)

@router.message(SurveyStates.question_14)
async def process_question_14(message: Message, state: FSMContext):
    await save_answer(message.from_user.id, 14, message.text)
    
    data = await state.get_data()
    answers = data.get("answers", {})
    answers[14] = message.text
    await state.update_data(answers=answers)
    
    await message.answer(
        "Вопрос 15: Что тебе может помочь сейчас? (можно выбрать несколько)",
        reply_markup=get_question_15_kb()
    )
    
    # Инициализируем список для хранения выбранных вариантов помощи
    await state.update_data(selected_helps=[])
    
    await state.set_state(SurveyStates.question_15)

@router.callback_query(F.data.startswith("help_"), SurveyStates.question_15)
async def process_help_selection(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_helps = data.get("selected_helps", [])
    
    if callback.data == "help_confirm":
        if not selected_helps:
            await callback.answer("Пожалуйста, выберите хотя бы один вариант")
            return
        
        # Сохраняем выбранные варианты помощи
        helps_str = ", ".join(selected_helps)
        await save_answer(callback.from_user.id, 15, helps_str)
        
        answers = data.get("answers", {})
        answers[15] = helps_str
        await state.update_data(answers=answers)

        await callback.message.answer(f"Вы выбрали: {helps_str}")
        
        await callback.message.answer(
            "Вопрос 16: Готов(а) ли ты вместо еды дать тебе то, что действительно нужно?",
            reply_markup=get_question_16_kb()
        )
        
        await state.set_state(SurveyStates.question_16)
    elif callback.data == "help_other":
        await callback.message.answer("Пожалуйста, напишите, что вам может помочь:")
        await state.set_state(SurveyStates.custom_answer)
        await state.update_data(custom_field="help")
    else:
        help_option = callback.data.replace("help_", "")
        
        # Преобразуем технические названия в читаемые
        help_names = {
            "sleep": "Сон",
            "walk": "Прогулка",
            "bath": "Ванная",
            "water": "Попить воды",
            "tea": "Чай",
            "massage": "Массаж",
            "selfcare": "Уход за собой",
            "movie": "Фильм или сериал",
            "vent": "Выговориться",
            "cry": "Поплакать",
            "write": "Написать свои эмоции"
        }
        
        readable_help = help_names.get(help_option, help_option)
        
        if readable_help in selected_helps:
            selected_helps.remove(readable_help)
            await callback.answer(f"Удалено: {readable_help}")
        else:
            selected_helps.append(readable_help)
            await callback.answer(f"Добавлено: {readable_help}")
        
        await state.update_data(selected_helps=selected_helps)
    
    await callback.answer()

@router.message(SurveyStates.question_16)
async def process_question_16(message: Message, state: FSMContext):
    await save_answer(message.from_user.id, 16, message.text)
    
    data = await state.get_data()
    answers = data.get("answers", {})
    answers[16] = message.text
    await state.update_data(answers=answers)
    
    # Формируем рекомендацию на основе ответа на последний вопрос
    recommendation = ""
    if message.text == "Да":
        recommendation = (
            "Позаботься о себе тем способом, который тебе ближе всего. "
            "Представь своего внутреннего ребенка, обними его, успокой и дай ему любовь. "
            "Пообещай ему, что ты будешь рядом и будешь слышать его. "
            "Похвали себя за то, что ты меняешься! Ты очень сильный и прекрасный человек! "
            "Как здорово, что ты есть у себя!"
        )
    elif message.text == "Нет":
        recommendation = (
            "Ты можешь разрешить себе съесть то, что ты хочешь, только попрошу об одном: "
            "Не вини себя! Сейчас это твой способ справляться с эмоциями. "
            "Уже здорово, что ты обращаешься к этому боту, когда тебе плохо. "
            "Ты не одна! Ты прекрасна просто потому, что ты есть, независимо от того, "
            "когда и сколько ты ешь. Ты - это не цифры на весах и не отражение в зеркале. "
            "Ты - это душа!"
        )
    else:  # "Не знаю"
        recommendation = (
            "Попробуй отвлечь себя. Загляни внутрь и попробуй понять, чего именно тебе сейчас не хватает? "
            "Представь рядом того, кто внутри просит о еде. Задай ему вопросы: "
            "Как я могу помочь тебе? Хочешь ли ты услышать, как сильно я люблю тебя? "
            "Попробуй высказать вслух или на бумаге все свои эмоции. "
            "Возможно, тебе в голову прийдет идея, как справиться с эмоциональным голодом сейчас. "
            "Если ты все-таки решила поесть - получи от этого максимум удовольствия."
        )
    
    # Сохраняем все ответы в базу данных
    await save_completed_survey(message.from_user.id, answers)
    
    # Отправляем рекомендацию и предложение запустить опрос снова
    await message.answer(
        f"{recommendation}\n\n"
        f"Когда тебе снова понадобится помощь, просто нажми /survey"
    )
    
    # Сбрасываем состояние
    await state.clear()
