from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import create_engine, Boolean, Column, Integer, String, Text


database_url="postgresql://eheidrich@/var/run/postgresql:5432/adsb_data"

engine = create_engine(database_url)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Session i think lets you create tables + stuff, gotta read up on it, but it’s something like this:

Base = declarative_base()

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	username = Column(String(255), unique=True, nullable=False)
	password = Column(String(255), nullable=False)
	email = Column(String(255))
	score = Column(Integer, default=0)
	created_at = Column(Integer, default=0)
	# disabled = Column(Boolean, default=False)
	token = Column(Text)
	datasets = relationship("Dataset", back_populates="users")
	elements = relationship("Element", back_populates="users") 

session = Session()
# allows you to interact with the database:
session.add(...)
session.commit()
