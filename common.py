from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from database.database import register_user, is_user_paid
from utils.states import SurveyStates, AdminStates
from keyboards.survey_kb import get_question_1_kb, get_admin_kb, get_payment_kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await register_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    )
    
    await message.answer(
        "👋 Привет! Я бот-помощник по интуитивному питанию.\n\n"
        "Я помогу тебе разобраться с твоими пищевыми привычками и эмоциональным состоянием.\n\n"
        "Чтобы начать опрос, отправь команду /survey"
    )
    
    # Сбрасываем состояние на случай, если пользователь был в середине опроса
    await state.clear()

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📋 Список доступных команд:\n\n"
        "/start - Начать взаимодействие с ботом\n"
        "/survey - Начать опрос по питанию\n"
        "/admin - Войти в панель администратора\n"
        "/payment - Оплатить доступ к полной версии\n"
        "/help - Показать это сообщение"
    )

@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    await message.answer("Введите пароль администратора:")
    await state.set_state(AdminStates.waiting_for_password)

@router.message(Command("payment"))
async def cmd_payment(message: Message):
    # Функционал оплаты временно отключен
    """
    is_paid = await is_user_paid(message.from_user.id)
    
    if is_paid:
        await message.answer("У вас уже есть доступ к полной версии программы. Спасибо за поддержку!")
    else:
        await message.answer(
            "Для получения полного доступа к программе питания необходимо произвести оплату.\n\n"
            "Стоимость: 1000 руб.\n\n"
            "Что вы получите:\n"
            "✅ Полный доступ к опросу по питанию\n"
            "✅ Персональные рекомендации\n"
            "✅ Поддержку в течение всего периода использования\n",
            reply_markup=get_payment_kb()
        )
    """
    # Временное сообщение вместо функционала оплаты
    await message.answer("⚠️ Функционал оплаты временно отключен. Все функции доступны бесплатно.")

@router.message(Command("survey"))
async def cmd_survey(message: Message, state: FSMContext):
    # Проверка оплаты временно отключена
    """
    # Проверяем, оплатил ли пользователь доступ
    is_paid = await is_user_paid(message.from_user.id)
    
    if not is_paid:
        await message.answer(
            "Для прохождения полного опроса необходимо оплатить доступ к программе.\n"
            "Отправьте /payment для оплаты."
        )
        return
    """
    
    # Начинаем опрос
    await message.answer(
        "Давай начнем опрос о твоем состоянии и отношении к питанию.\n\n"
        "Вопрос 1: Я хочу поесть:",
        reply_markup=get_question_1_kb()
    )
    
    # Устанавливаем состояние первого вопроса
    await state.set_state(SurveyStates.question_1)
    
    # Инициализируем словарь для хранения ответов
    await state.update_data(answers={})

@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state is None:
        await message.answer("Нет активного процесса для отмены.")
        return
    
    from aiogram.types import ReplyKeyboardRemove
    
    await state.clear()
    await message.answer(
        "Действие отменено. Вы можете начать заново, используя соответствующую команду.",
        reply_markup=ReplyKeyboardRemove()  # Удаляем клавиатуру
    )
