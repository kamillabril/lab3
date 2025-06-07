import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Weather, SunInfo  # Замініть на правильний імпорт моделей

# Підключення до бази даних (замініть на відповідні дані)
DATABASE_URL = 'postgresql://postgres:1234@localhost:5433/weather_db'

# Створення підключення до бази даних
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Завантаження даних з CSV файлу
weather_data = pd.read_csv('C:/Users/))))/Documents/GitHub/Lab3_bd/GlobalWeatherRepository.csv')

# Функція для перевірки, чи варто виходити на вулицю
def calculate_should_go_outside(wind_kph: float) -> bool:
    # Перевіряємо, чи wind_kph <= 10
    if wind_kph <= 10:
        return True  # Можна виходити на вулицю
    return False  # Ні, не можна виходити на вулицю

# Ітеруємо через рядки погодних даних
for _, row in weather_data.iterrows():
    # Форматуємо дані для вставки в таблицю Weather
    weather = Weather(
        id=row['weather_id'],
        country=row['country'],
        wind_kph=row['wind_kph'],
        wind_degree=row['wind_degree'],
        wind_direction=row['wind_direction'],
        last_updated=datetime.strptime(row['last_updated'], '%Y-%m-%d %H:%M:%S'),
    )

    # Рахуємо, чи варто виходити на вулицю
    should_go_outside = calculate_should_go_outside(row['wind_kph'])

    # Створюємо запис для SunInfo
    sun_info = SunInfo(
        weather_id=row['Weather_id'],
        sunrise=datetime.strptime(row['sunrise'], '%I:%M %p') if row['sunrise'] != 'No sunrise' else None,
        sunset=datetime.strptime(row['sunset'], '%I:%M %p') if row['sunset'] != 'No sunset' else None,
        moonrise=datetime.strptime(row['moonrise'], '%I:%M %p') if row['moonrise'] != 'No moonrise' else None,
        moonset=datetime.strptime(row['moonset'], '%I:%M %p') if row['moonset'] != 'No moonset' else None,
        should_go_outside=should_go_outside
    )

    # Додаємо в сесію
    session.add(weather)
    session.add(sun_info)

# Зберігаємо зміни
session.commit()

# Закриваємо сесію
session.close()
