from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine import URL
from opensky_api import OpenSkyApi
import pandas as pd
# Step 1: Define SQLAlchemy engine to connect to PostgreSQL database
# Replace 'username', 'password', 'host', 'port', and 'database_name' with your actual credentials

url = URL.create(
    drivername="postgresql",
    username="ehong",
    password="Elanlofr0gs!",
    host="/var/run/postgresql/",
    database="adsb_data"
)

engine = create_engine(url)

Base = declarative_base()

metadata = MetaData()
table_name = 'flights'

class Flight(Base):
	__tablename__ = table_name
	icao24 = Column(String, primary_key=True)
	latitude = Column(String)
	longitude = Column(String)
	time_position = Column(Integer)
	on_ground = Column(Boolean)

Base.metadata.create_all(engine)
api = OpenSkyApi()
states = api.get_states().states

state_dicts = [s.__dict__ for s in states]

df = pd.DataFrame(state_dicts)
# data = api.get_flights_from_interval(1517227200, 1517230800)
# for flight in data:
#     print(flight)

df = df[['icao24', 'longitude', 'latitude', 'time_position', 'on_ground']]



df.to_sql(table_name,
		con=engine,
		index=False,
		index_label='id',
		if_exists='replace')
