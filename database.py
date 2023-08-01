from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

dbschema = 'public'

DATABASE_URL = 'postgresql://postgres:1234567890@localhost:5432/testdb'

engine = create_engine(DATABASE_URL, echo=True)

session = sessionmaker(bind=engine)

Base =declarative_base()

db = session()