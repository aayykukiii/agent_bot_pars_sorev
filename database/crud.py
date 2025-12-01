from sqlalchemy.orm import Session
from .models import Vacancy, Skill, User, Favorite



# vacancy
def create_vacancy(db: Session, title: str, description: str = None, salary: int = None, url: str = None, skills=[]):
    vacancy = Vacancy(title=title, description=description, salary=salary, url=url)
    for skill in skills:
        vacancy.skills.append(skill)
    db.add(vacancy)
    db.commit()
    db.refresh(vacancy)
    return vacancy

def get_vacancies(db: Session):
    return db.query(Vacancy).all()

def update_vacancy(db: Session, vacancy_id: int, **kwargs):
    vacancy = db.query(Vacancy).get(vacancy_id)
    if not vacancy:
        return None
    for key, value in kwargs.items():
        setattr(vacancy, key, value)
    db.commit()
    db.refresh(vacancy)
    return vacancy

def delete_vacancy(db: Session, vacancy_id: int):
    vacancy = db.query(Vacancy).get(vacancy_id)
    if not vacancy:
        return False
    db.delete(vacancy)
    db.commit()
    return True



# skill
def create_skill(db: Session, name: str):
    skill = Skill(name=name)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill

def get_skills(db: Session):
    return db.query(Skill).all()



# user
def create_user(db: Session, telegram_id: int, username: str = None):
    user = User(telegram_id=telegram_id, username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session):
    return db.query(User).all()



# favorite

def add_favorite(db: Session, user: User, vacancy: Vacancy):
    fav = Favorite(user=user, vacancy=vacancy)
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return fav

def get_user_favorites(db: Session, user: User):
    return db.query(Favorite).filter(Favorite.user_id == user.id).all()
