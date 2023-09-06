from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True)
    status = Column(Integer)


# class State(Base):
#     __tablename__ = "states"

#     id = Column(Integer, autoincrement=True, primary_key=True, index=True)
#     name = Column(String, unique=True)
#     state = Column(Integer)

