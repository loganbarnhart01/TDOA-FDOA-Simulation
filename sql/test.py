from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import create_engine, Boolean, Column, Integer, String, Text, Float
from pandas import pandas as pd

database_url="postgresql://ehong@/var/run/postgresql:5432/adsb_data"

engine = create_engine(database_url)
conn = engine.connect()
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Session i think lets you create tables + stuff, gotta read up on it, but it’s something like this:

Base = declarative_base()

class Flight(Base):
	__tablename__ = "flights"

	icao24 = Column(String(255), nullable=True)
	callsign = Column(String(255), nullable=True)
	origin_country = Column(String(255), nullable=True)
	time_position = Column(Float, nullable=False)
	last_contact = Column(Float, nullable=True)
	longitude = Column(Float, nullable=False)
	latitude = Column(Float, nullable=False)
	baro_altitude = Column(Float, nullable=True)
	on_ground = Column(Boolean, nullable=True)
	velocity = Column(Float, nullable=True)
	true_track = Column(Float, nullable=True)
	vertical_rate = Column(Float, nullable=True)
	sensors = Column(Float, nullable=True)
	geo_altitude = Column(Float, nullable=True)
	squawk = Column(Integer, nullable=True)
	spi = Column(Boolean, nullable=True)
	position_source = Column(Integer, nullable=True)
	category = Column(Integer, nullable=True)

session = Session()
# allows you to interact with the database:
session.add(...)
session.commit()
