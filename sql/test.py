
'''
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

'''

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean
import pandas as pd
# Step 1: Define SQLAlchemy engine to connect to PostgreSQL database
# Replace 'username', 'password', 'host', 'port', and 'database_name' with your actual credentials

engine = create_engine('postgresql://eheidrich:EjhRhody8@@/adsb_data?host=/var/run/postgresql/')
# Step 2: Define metadata and table structure
metadata = MetaData()
table_name = 'flights'
your_table = Table(table_name, metadata,
					Column("ICAO24", String(255), nullable=True),
					Column('callsign', String(255), nullable=True),
					Column("origin_country", String(255), nullable=True),
					Column("time_position", Float, nullable=False),
					Column("last_contact", Float, nullable=True),
					Column("longitude", Float, nullable=False),
					Column('latitude', Float, nullable=False),
					Column('baro_altitude', Float, nullable=True),
					Column("on ground", Boolean, nullable=True),
					Column("velocity", Float, nullable=True),
					Column("true track", Float, nullable=True),
					Column("vertical rate", Float, nullable=True),
					Column("sensors", Float, nullable=True),
					Column("geo altitude",Float, nullable=True),
					Column("squawk", Integer, nullable=True),
					Column("spi", Boolean, nullable=True),
					Column("position source", Integer, nullable=True),
					Column("category", Integer, nullable=True),
                   )

# Step 3: Read CSV file into a Pandas DataFrame
csv_file_path = '/home/eheidrich/Documents/Flight-Tracker-Simulator/flight_data/adsb_data.csv'
data = pd.read_csv(csv_file_path)

# Step 4: Insert data from DataFrame into PostgreSQL database table
with engine.connect() as connection:
    # Create table in the database (if not exists)
    metadata.create_all(engine)
    
    # Insert data into the table
    data.to_sql(table_name, connection, if_exists='append', index=False)