from sqlalchemy import *
from sqlalchemy.sql import *
from database import Base
from database import dbschema

class CompleteLoginData(Base) :
     __tablename__ = 'completedata'
     __table_args__ = {'schema' : dbschema}
     UploadId = Column(Integer, primary_key=True,autoincrement=True)
     Username = Column(String)
     Password = Column(String)