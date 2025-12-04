from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from states.user_states import FindState

# импорт твоего парсинга
from parsing_vakanc.pars import parse_habr_career
from parsing_vakanc.pars import pars_superjob_grozny
import asyncio

router = Router()

# 🔍 Старт поиска
@router.callback_query(F.data == "call_find")
async def call_find_handler(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите язык (например: Python, Java, C++, PHP):")
    await state.set_state(FindState.waiting_language)
    await call.answer()


# 📝 Шаг 1 — язык
@router.message(FindState.waiting_language)
async def find_language_handler(message: Message, state: FSMContext):
    await state.update_data(language=message.text.strip())
    await message.answer("Введите минимальную зарплату (только число, например: 150000):")
    await state.set_state(FindState.waiting_salary)


# 💰 Шаг 2 — зарплата
@router.message(FindState.waiting_salary)
async def find_salary_handler(message: Message, state: FSMContext):
    await state.update_data(salary=message.text.strip())
    await message.answer("Формат работы? (удалённо / офис / гибрид):")
    await state.set_state(FindState.waiting_format)


# 🏢 Шаг 3 — формат
@router.message(FindState.waiting_format)
async def find_format_handler(message: Message, state: FSMContext):
    await state.update_data(format=message.text.strip())
    await message.answer("За сколько последних дней искать вакансии? (например: 7):")
    await state.set_state(FindState.waiting_days)


# 🕒 Шаг 4 — период + запуск парсинга
@router.message(FindState.waiting_days)
async def find_days_handler(message: Message, state: FSMContext):
    await state.update_data(days=message.text.strip())
    data = await state.get_data()

    lang = data["language"]
    salary = data["salary"]
    work_format = data["format"]
    days = data["days"]

    await message.answer(
        f"🔎 Выполняю поиск вакансий...\n\n"
        f"Язык: {lang}\n"
        f"Зарплата от: {salary}\n"
        f"Формат: {work_format}\n"
        f"Период: {days} дней\n"
        f"⏳ Подождите 5–15 секунд..."
    )

    # URL'ы твоих сайтов
    habr_url = "https://career.habr.com/vacancies"
    superjob_url = "https://grozniy.superjob.ru/vacancy/search/?click_from=facet"

    # Запуск парсеров параллельно
    habr_result, sj_result = await asyncio.gather(
        parse_habr_career(habr_url),
        pars_superjob_grozny(superjob_url)
    )

    await message.answer(
        f"✨ Готово!\n\n"
        f"📌 Habr Career: найдено {habr_result}\n"
        f"📌 SuperJob Грозный: найдено {sj_result}"
    )

    await state.clear()
