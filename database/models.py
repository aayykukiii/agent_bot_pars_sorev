from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base



# Связующая таблица many-to-many
vacancy_skill = Table(
    "vacancy_skill",
    Base.metadata,
    Column("vacancy_id", Integer, ForeignKey("vacancies.id", ondelete="CASCADE")),
    Column("skill_id", Integer, ForeignKey("skills.id", ondelete="CASCADE")),
)



# Таблица Skills
class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    vacancies = relationship(
        "Vacancy",
        secondary=vacancy_skill,
        back_populates="skills"
    )

    def __repr__(self):
        return f"<Skill(id={self.id}, name={self.name})>"



# Таблица Vacancies
class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    salary = Column(Integer, nullable=True)
    url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    skills = relationship(
        "Skill",
        secondary=vacancy_skill,
        back_populates="vacancies"
    )

    favorites = relationship("Favorite", back_populates="vacancy", cascade="all, delete")

    def __repr__(self):
        return f"<Vacancy(id={self.id}, title={self.title})>"



# Таблица Users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    favorites = relationship("Favorite", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id})>"



# Таблица Favorites
class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    vacancy_id = Column(Integer, ForeignKey("vacancies.id", ondelete="CASCADE"))
    added_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites")
    vacancy = relationship("Vacancy", back_populates="favorites")

    def __repr__(self):
        return f"<Favorite(user_id={self.user_id}, vacancy_id={self.vacancy_id})>"