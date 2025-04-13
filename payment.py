from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, SuccessfulPayment
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database.database import record_payment, update_payment_status

router = Router()

# Константы для платежей (в реальном проекте лучше хранить в переменных окружения)
PAYMENT_TOKEN = "YOUR_PAYMENT_TOKEN"  # Токен от платежной системы (например, от Stripe)
PRICE = 1000  # Цена в рублях

@router.callback_query(F.data == "pay")
async def process_payment(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    
    # Проверяем, настроен ли платежный токен
    if PAYMENT_TOKEN.startswith('YOUR_'):
        await callback.message.answer(
            "⚠️ Платежи временно недоступны. Пожалуйста, свяжитесь с администратором."
        )
        return
    
    # Создаем счет на оплату через Telegram Payments API
    # Функционал оплаты временно отключен
    """
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Программа по питанию",
        description="Полный доступ к программе по питанию и эмоциональному состоянию",
        payload=f"payment_user_{callback.from_user.id}",
        provider_token=PAYMENT_TOKEN,
        currency="RUB",
        prices=[
            LabeledPrice(
                label="Программа по питанию",
                amount=PRICE * 100  # Сумма в копейках
            )
        ],
        start_parameter="nutrition_program",
        provider_data=None,
        photo_url="https://example.com/nutrition_program.jpg",  # URL изображения для счета (замените на реальный)
        photo_size=600,
        photo_width=800,
        photo_height=450,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_markup=None
    )
    """
    
    # Временное сообщение вместо оплаты
    await callback.message.answer("⚠️ Функционал оплаты временно отключен. Пожалуйста, свяжитесь с администратором.")
    
    # Записываем информацию о платеже в базу данных
    # await record_payment(callback.from_user.id, PRICE)

# Обработчик предварительной проверки платежа
@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    # Здесь можно проверить, все ли в порядке с платежом
    # Например, доступен ли товар, правильная ли сумма и т.д.
    
    # Функционал оплаты временно отключен
    """
    # Для демонстрации просто подтверждаем все платежи
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    """
    pass

# Обработчик успешного платежа
@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    # Функционал оплаты временно отключен
    """
    payment_info = message.successful_payment
    
    # Обновляем статус платежа в базе данных
    await update_payment_status(message.from_user.id, "completed")
    
    # Отправляем сообщение об успешной оплате
    await message.answer(
        f"✅ Платеж на сумму {payment_info.total_amount / 100} {payment_info.currency} успешно выполнен!\n\n"
        "Теперь у вас есть полный доступ к программе питания.\n"
        "Вы можете начать опрос, отправив команду /survey"
    )
    """
    pass

@router.callback_query(F.data == "cancel_payment")
async def cancel_payment(callback: CallbackQuery):
    await callback.answer()
    
    await callback.message.answer("Оплата отменена. Вы можете вернуться к ней позже через команду /payment")
