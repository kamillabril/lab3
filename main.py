from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # Імпортуємо наші моделі

# Підключення до БД
DATABASE_URI = 'postgresql://username:password@localhost/mydatabase'
engine = create_engine(DATABASE_URI)

# Створення сесії
Session = sessionmaker(bind=engine)
session = Session()

# Створення таблиць у базі даних
Base.metadata.create_all(engine)