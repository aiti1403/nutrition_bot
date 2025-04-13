from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import csv
import io
import os
from utils.states import AdminStates
from keyboards.survey_kb import get_admin_kb
from database.database import get_all_completed_surveys

router = Router()

# Пароль для входа в админку
ADMIN_PASSWORD = "admin123"

@router.message(AdminStates.waiting_for_password)
async def check_admin_password(message: Message, state: FSMContext):
    if message.text == ADMIN_PASSWORD:
        await message.answer(
            "Вход в панель администратора выполнен успешно!",
            reply_markup=get_admin_kb()
        )
        await state.set_state(AdminStates.admin_menu)
    else:
        await message.answer(
            "Неверный пароль. Доступ запрещен.",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()

@router.message(AdminStates.admin_menu, F.text == "Просмотр результатов")
async def view_results(message: Message, state: FSMContext):
    surveys = await get_all_completed_surveys()
    
    if not surveys:
        await message.answer("Пока нет завершенных опросов.")
        return
    
    # Отправляем информацию о последних 5 опросах
    response = "Последние опросы:\n\n"
    for i, survey in enumerate(surveys[:5], 1):
        response += f"{i}. Пользователь: {survey['first_name']} {survey['last_name']} (@{survey['username']})\n"
        response += f"   Дата: {survey['completion_date']}\n"
        response += f"   ID опроса: {survey['id']}\n\n"
    
    await message.answer(response)
    # Возвращаем пользователя в меню админа после просмотра результатов
    await message.answer("Выберите действие:", reply_markup=get_admin_kb())
    await state.set_state(AdminStates.admin_menu)

@router.message(AdminStates.view_results)
async def handle_view_results_state(message: Message, state: FSMContext):
    # Возвращаем пользователя в меню админа при любом сообщении в состоянии просмотра результатов
    await message.answer("Возвращаемся в меню администратора", reply_markup=get_admin_kb())
    await state.set_state(AdminStates.admin_menu)

@router.message(AdminStates.admin_menu, F.text == "Экспорт данных")
async def export_data(message: Message):
    surveys = await get_all_completed_surveys()
    
    if not surveys:
        await message.answer("Нет данных для экспорта.")
        return
    
    # Создаем временный файл на диске
    filename = "survey_results.csv"
    
    # Открываем файл для записи с указанием кодировки
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        
        # Записываем заголовки
        headers = ["ID", "User ID", "Username", "First Name", "Last Name", "Completion Date"]
        for i in range(1, 17):
            headers.append(f"Question {i}")
        writer.writerow(headers)
        
        # Записываем данные
        for survey in surveys:
            row = [
                survey["id"],
                survey["user_id"],
                survey["username"],
                survey["first_name"],
                survey["last_name"],
                survey["completion_date"]
            ]
            
            # Добавляем ответы на вопросы
            for i in range(1, 17):
                row.append(survey["survey_data"].get(str(i), ""))
            
            writer.writerow(row)
    
    # Отправляем файл
    file = FSInputFile(filename)
    await message.answer_document(file)
    
    # Удаляем временный файл после отправки
    try:
        os.remove(filename)
    except Exception as e:
        print(f"Ошибка при удалении временного файла: {e}")

@router.message(AdminStates.admin_menu, F.text == "Выход из админки")
async def exit_admin(message: Message, state: FSMContext):
    # Очищаем состояние перед отправкой сообщения
    await state.clear()
    
    # Отправляем сообщение с удалением клавиатуры
    await message.answer(
        "Вы вышли из панели администратора.",
        reply_markup=ReplyKeyboardRemove()
    )

# Добавляем обработчик для любых других сообщений в меню админа
@router.message(AdminStates.admin_menu)
async def unknown_admin_command(message: Message):
    await message.answer(
        "Неизвестная команда. Пожалуйста, используйте кнопки меню.",
        reply_markup=get_admin_kb()
    )
