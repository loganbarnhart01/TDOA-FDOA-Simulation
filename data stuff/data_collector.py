# make table in sql

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL
from opensky_api import OpenSkyApi
import time
import pandas as pd

url = URL.create(
    drivername="postgresql",
    username="eheidrich",
    password="EjhRhody8@!",
    host="/var/run/postgresql/",
    database="adsb_data"
)

engine = create_engine(url)

Session = sessionmaker(bind=engine)

db = Session()

table_name = 'flights'

Base = declarative_base()

def data_collector():
	Base.metadata.create_all(engine)

	while True:
		api = OpenSkyApi()
		states = api.get_states().states

		for s in states:
			create_flight(s.icao24, s.latitude, s.longitude, s.time_position, s.on_ground)

		time.sleep(10)

class Flight(Base):
	__tablename__ = table_name
	icao24 = Column(String, primary_key=True)
	latitude = Column(String)
	longitude = Column(String)
	time_position = Column(Integer)
	on_ground = Column(Boolean)

def create_flight(icao24, latitude, longitude, time_position, on_ground):
	print(icao24, latitude, longitude, time_position, on_ground)
	query = db.query(Flight).filter_by(icao24 = icao24).first()
	if on_ground == True:
		if query:
			delete_flight(icao24)
		return
	
	if latitude == None or longitude == None or time_position == None:
		return

	if query:
		#flight in table already
		update_flight(icao24=icao24, latitude=latitude, longitude=longitude, time_position=time_position)

	else:
		new_flight = Flight(icao24=icao24, latitude=latitude, longitude=longitude, time_position=time_position, on_ground=on_ground)
		db.add(new_flight)
		db.commit()

def update_flight(icao24, latitude, longitude, time_position):
	flight = db.query(Flight).filter_by(icao24 = icao24).first()
	if flight:
		curr_lat = flight.latitude.split()
		if len(curr_lat) == 10:
			flight.latitude = ','.join(curr_lat[1:] + [latitude])
		else:
			curr_lat.append(latitude)
			flight.latitude = ','.join(curr_lat)

def delete_flight(icao24):
	flight = db.query(Flight).filter_by(icao24 = icao24).first()
	if flight:
		db.delete(flight)

def cleanup_table():
	flights = db.query(Flight).filter_by(on_ground =True).all()

	for flight in flights:
		db.delete(flight)
		
data_collector()
