from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    #если после проверки id, не совпал с админом, то выводим клаву для юзера
    text = (
        "🔥 Добро пожаловать в бот, который подбирает вакансии специально для вас!\n\n"
        "Здесь вы получите вакансии, подходящие под ваши навыки, опыт и предпочтения.\n\n"
        "Доступные команды:\n"
        "/find — поиск с фильтрами (язык, зарплата, формат, дата)\n"
        "/favorites — избранные вакансии\n"
        "/register - регистрация\n"
        "/vacancy display — здесь будут вакансии для вас\n"
        "/show more — загрузка следующих вакансий\n"
        "/add to favorites — сохранить вакансию\n"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="find", callback_data="call_find")],
        [InlineKeyboardButton(text="favorites", callback_data="call_favorites")],
        [InlineKeyboardButton(text="register", callback_data="register")],
        [InlineKeyboardButton(text="vacancy display", callback_data="reviews")],
        [InlineKeyboardButton(text="show more", callback_data="more")],
        [InlineKeyboardButton(text="add to favorites", callback_data="add_favorites")],
    ])
    
    await message.answer(text, reply_markup=keyboard)
