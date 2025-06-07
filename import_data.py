import csv
from sqlalchemy.orm import sessionmaker
from models import Weather, SunInfo, engine

# Створюємо сесію
Session = sessionmaker(bind=engine)
session = Session()

from datetime import datetime

def convert_time(value):
    if value == "No moonset" or value == "No moonrise":
        return None  # Якщо значення некоректне, замінюємо на None
    try:
        # Перетворюємо значення часу з формату '4:50:00 AM' на об'єкт типу time
        return datetime.strptime(value, "%I:%M:%S %p").time()
    except ValueError:
        return None  # Якщо не вдається перетворити, повертаємо None

# Відкриваємо CSV-файл
with open("GlobalWeatherRepository.csv", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        # Додаємо в таблицю Weather
        weather_entry = Weather(
            country=row["country"],
            last_updated=row["last_updated"]
        )


        session.add(weather_entry)


        # Додаємо в таблицю SunInfo
        sun_info_entry = SunInfo(
            weather_id=weather_entry.id,  # Використовуємо ID щойно створеного Weather
            sunrise=convert_time(row["sunrise"]),
            sunset=convert_time(row["sunset"]),
            moonrise=convert_time(row["moonrise"]),
            moonset=convert_time(row["moonset"]),
            should_go_outside=None  # Логіку визначення ще додамо
        )
        session.add(sun_info_entry)

    session.commit()

print("✅ Дані успішно імпортовані!")
