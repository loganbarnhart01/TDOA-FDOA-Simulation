from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL

Base = declarative_base()

class Flight(Base):
	__tablename__ = 'flights'
	icao24 = Column(String, primary_key=True)
	latitude = Column(String)
	longitude = Column(String)
	time_position = Column(Integer)
	on_ground = Column(Boolean)
	
def create_table():
	url = URL.create(
    drivername="postgresql",
    username="ehong",
    password="Elanlofr0gs!",
    host="/var/run/postgresql/",
    database="adsb_data"
)

	engine = create_engine(url)

	Session = sessionmaker(bind=engine)

	db = Session()
	
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)