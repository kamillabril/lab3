from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()


class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    country = Column(String, nullable=False)
    last_updated = Column(DateTime, nullable=False)
    sun_info = relationship("SunInfo", back_populates="weather", uselist=False)
    weather_data = relationship("WeatherData", back_populates="weather", uselist=False)


class SunInfo(Base):
    __tablename__ = 'sun_info'

    id = Column(Integer, primary_key=True)
    weather_id = Column(Integer, ForeignKey('weather.id'), nullable=False)
    sunrise = Column(Time, nullable=False)
    sunset = Column(Time, nullable=False)
    moonrise = Column(Time)
    moonset = Column(Time)
    should_go_outside = Column(Boolean, default=None)
    is_good_weather = Column(Boolean, default=None)  # Нова колонка

    weather = relationship("Weather", back_populates="sun_info")


class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    weather_id = Column(Integer, ForeignKey('weather.id'), nullable=False)
    wind_kph = Column(Float, nullable=False)
    wind_degree = Column(Integer, nullable=False)
    wind_direction = Column(String, nullable=False)
    uv_index = Column(Integer, nullable=False)

    weather = relationship("Weather", back_populates="weather_data")


# Підключення до БД
DATABASE_URL = "postgresql://postgres:1234@localhost:5433/weather_db"
engine = create_engine(DATABASE_URL)

# Створення сесії
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
