from aiogram.fsm.state import State, StatesGroup

class SurveyStates(StatesGroup):
    # Состояния для вопросов опроса
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    question_8 = State()
    question_9 = State()
    question_10 = State()
    question_11 = State()
    question_12 = State()
    question_13 = State()
    question_14 = State()
    question_15 = State()
    question_16 = State()
    custom_answer = State()  # Для ввода пользовательских ответов

class AdminStates(StatesGroup):
    waiting_for_password = State()
    admin_menu = State()
    view_results = State()
    export_data = State()

class PaymentStates(StatesGroup):
    waiting_for_payment = State()
    payment_confirmation = State()
