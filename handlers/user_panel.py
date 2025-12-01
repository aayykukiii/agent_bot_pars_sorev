from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from config import ID_ADMIN


router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    #проверка на админа
    if message.from_user.id == ID_ADMIN:
        username = message.from_user.username or message.from_user.full_name or "admin"
        text = f"Здравствуйте, {username} (id: {message.from_user.id}). Выберите действие:"
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="просмотр вакансий", callback_data="read_vacancies")],
            [InlineKeyboardButton(text="удаление", callback_data="delete_vacancy")],
        ])
        await message.answer(text, reply_markup=kb)
        return

    #если после проверки id, не совпал с админом, то выводим клаву для юзера
    text = (
        "🔥 Добро пожаловать в бот, который подбирает вакансии специально для вас!\n\n"
        "Здесь вы получите вакансии, подходящие под ваши навыки, опыт и предпочтения.\n\n"
        "Доступные команды:\n"
        "/find — поиск с фильтрами (язык, зарплата, формат, дата)\n"
        "/favorites — избранные вакансии\n"
        "показ вакансий — здесь будут вакансии для вас\n"
        "показать ещё — загрузка следующих вакансий\n"
        "добавить в избранное — сохранить вакансию\n"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="find", callback_data="call_find")],
        [InlineKeyboardButton(text="favorites", callback_data="call_favorites")],
        [InlineKeyboardButton(text="показ вакансий", callback_data="reviews")],
        [InlineKeyboardButton(text="показать еще", callback_data="more")],
        [InlineKeyboardButton(text="добавить избранное", callback_data="add_favorites")],
    ])
    
    await message.answer(text, reply_markup=keyboard)
