from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config import ID_ADMIN
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(Command("admin"))
async def admin_cmd(message: Message):
    if message.from_user.id == ID_ADMIN:
        username = message.from_user.username or message.from_user.full_name or "admin"
        text = f"Здравствуйте, {username} (id: {message.from_user.id}). Выберите действие:"
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="просмотр вакансий", callback_data="read_vacancies")],
            [InlineKeyboardButton(text="удаление", callback_data="delete_vacancy")],
        ])
        await message.answer(text, reply_markup=kb)
    else:
        await message.answer("У тебя нет прав.")
