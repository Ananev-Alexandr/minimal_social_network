from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@" \
                              f"{os.getenv('POSTGRES_HOST')}:5432/{os.getenv('POSTGRES_DB')}"

# Движок БД                             
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Для миграции устанавливаем Alembic, инициализируем его "alembic init alembic",

# alembic init migration
# В файле alembic.ini прописываем URL БД
# alembic revision --autogenerate -m 'login delete'
# alembic upgrade head