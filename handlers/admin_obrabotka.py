# from aiogram import Router, F
# from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.fsm.context import FSMContext

# from config import ID_ADMIN
# from database import crud



# @router.callback_query(F.data == "admin_vacancies")
# async def admin_show_vacancies(callback: CallbackQuery):
#     data = get_vacancies()

#     if not data:
#         return await callback.message.answer("Нет вакансий.")

#     for v_id, title, company, salary in data:
#         text = (
#             f"<b>{title}</b>\n"
#             f"{company}\n"
#             f"Зарплата: {salary}"
#         )
#         await callback.message.answer(text, reply_markup=vacancy_keyboard(v_id))
# просмотр вакансий



# def vacancy_keyboard(v_id):
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_{v_id}")]
#     ])
# кнопка удаления под каждой вакансией