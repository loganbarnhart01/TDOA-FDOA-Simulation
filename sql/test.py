from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean
from sqlalchemy.engine import URL
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

# engine = create_engine('postgresql://ehong:Elanlofr0gs!@@/adsb_data?host=/var/run/postgresql/')
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


csv_file_path = '/home/ehong/Downloads/Flight-Tracker-Simulator/flight_data/adsb_data.csv'

with open(csv_file_path, 'r') as file:
    df = pd.read_csv(file)


df.to_sql(table_name,
          con=engine,
          index=False,
          index_label='id',
          if_exists='replace')
