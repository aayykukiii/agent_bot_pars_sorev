from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database.db import SessionLocal
from database import crud
from parsing_vakanc.pars import parse_habr_career, pars_superjob_grozny


router = Router()



def render_vacancy(v):
    skills = ", ".join([s.name for s in v.skills]) or "нет навыков"

    return (
        f"📌 Вакансия #{v.id}\n\n"
        f"📎 Название: {v.title}\n"
        f"📝 Описание: {v.description}\n"
        f"💰 Зарплата: {v.salary}\n"
        f"🧩 Навыки: {skills}\n"
        f"🔗 URL: {v.url}"
    )



@router.callback_query(F.data == "read_vacancies")
async def read_vacancies(callback: CallbackQuery):
    # Парсим вакансии с сайтов и сохраняем новые в БД
    await callback.answer("🔄 Обновляю вакансии с сайтов...")

    # Собираем результаты парсеров
    results = []
    # Habr Career
    try:
        res1 = await parse_habr_career('https://career.habr.com/vacancies')
        count1 = len(res1) if isinstance(res1, list) else 0
        await callback.message.answer(f"Парсер Habr: найдено {count1}")
        if res1:
            results.extend(res1)
    except Exception as e:
        await callback.message.answer(f"Ошибка парсера Habr: {e}")

    # SuperJob Grozny
    try:
        res2 = await pars_superjob_grozny('https://grozniy.superjob.ru/vacancy/search/?click_from=facet')
        count2 = len(res2) if isinstance(res2, list) else 0
        await callback.message.answer(f"Парсер SuperJob: найдено {count2}")
        if res2:
            results.extend(res2)
    except Exception as e:
        await callback.message.answer(f"Ошибка парсера SuperJob: {e}")

    db = SessionLocal()

    # Сохраняем новые вакансии (по уникальному URL)
    added = 0
    for item in results:
        try:
            url = item.get('url') or ""
            if not url or url == "#":
                # если нет валидного url — пытаемся по названию пропускать дубликаты
                exists = db.query(crud.Vacancy).filter(crud.Vacancy.title == item.get('title')).first()
            else:
                exists = db.query(crud.Vacancy).filter(crud.Vacancy.url == url).first()

            if exists:
                continue

            # подготовка навыков
            skill_objs = []
            for sname in item.get('skills', []) or []:
                sname = sname.strip()
                if not sname:
                    continue
                sk = db.query(crud.Skill).filter(crud.Skill.name == sname).first()
                if not sk:
                    sk = crud.create_skill(db, sname)
                skill_objs.append(sk)

            crud.create_vacancy(
                db,
                title=item.get('title') or 'Без названия',
                description=item.get('description'),
                salary=item.get('salary'),
                url=url,
                skills=skill_objs
            )
            added += 1
        except Exception:
            continue
    vacancies = db.query(crud.Vacancy).order_by(crud.Vacancy.id).all()

    total_found = len(results)

    # Отчёт администратору — сколько найдено и добавлено
    await callback.message.answer(f"🔔 Обновление завершено. Найдено: {total_found}. Добавлено новых: {added}.")

    if not vacancies:
        await callback.message.answer("❌ Вакансий нет")
        db.close()
        return

    # Отправляем первую вакансию как новое сообщение (на случай, если edit_text не срабатывает)
    v = vacancies[0]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data=f"prev_{v.id}"),
            InlineKeyboardButton(text="▶️ Следующая", callback_data=f"next_{v.id}")
        ],
        [
            InlineKeyboardButton(text="🗑 Удалить", callback_data=f"del_{v.id}")
        ]
    ])

    await callback.message.answer(render_vacancy(v), reply_markup=kb)
    db.close()




# показать вакансию по ID

async def show_vacancy(callback: CallbackQuery, vac_id: int):

    db = SessionLocal()
    vacancies = db.query(crud.Vacancy).order_by(crud.Vacancy.id).all()
    ids = [v.id for v in vacancies]

    if vac_id not in ids:
        await callback.answer("Ошибка: вакансия не найдена")
        db.close()
        return

    index = ids.index(vac_id)
    v = vacancies[index]

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data=f"prev_{v.id}"),
            InlineKeyboardButton(text="▶️ Следующая", callback_data=f"next_{v.id}")
        ],
        [
            InlineKeyboardButton(text="🗑 Удалить", callback_data=f"del_{v.id}")
        ]
    ])

    await callback.message.edit_text(
        render_vacancy(v),
        reply_markup=kb
    )

    db.close()



# следующая

@router.callback_query(F.data.startswith("next_"))
async def next_v(callback: CallbackQuery):

    cur = int(callback.data.replace("next_", ""))

    db = SessionLocal()
    vacancies = db.query(crud.Vacancy).order_by(crud.Vacancy.id).all()
    ids = [v.id for v in vacancies]
    db.close()

    i = ids.index(cur)

    if i + 1 >= len(ids):
        await callback.answer("Это последняя вакансия")
        return

    await show_vacancy(callback, ids[i+1])




# предыдущая

@router.callback_query(F.data.startswith("prev_"))
async def prev_v(callback: CallbackQuery):

    cur = int(callback.data.replace("prev_", ""))

    db = SessionLocal()
    vacancies = db.query(crud.Vacancy).order_by(crud.Vacancy.id).all()
    ids = [v.id for v in vacancies]
    db.close()

    i = ids.index(cur)

    if i == 0:
        await callback.answer("Это первая вакансия")
        return

    await show_vacancy(callback, ids[i-1])



@router.callback_query(F.data.startswith("del_"))
async def delete_v(callback: CallbackQuery):

    vac_id = int(callback.data.replace("del_", ""))

    db = SessionLocal()
    ok = crud.delete_vacancy(db, vac_id)

    if not ok:
        await callback.message.answer("Ошибка: вакансия не найдена")
        db.close()
        return

    vacancies = db.query(crud.Vacancy).order_by(crud.Vacancy.id).all()
    db.close()

    if not vacancies:
        await callback.message.edit_text("✅ Все вакансии удалены")
        return

    await show_vacancy(callback, vacancies[0].id)
