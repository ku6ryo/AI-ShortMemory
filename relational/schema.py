from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from relational.tables.message import Message

DATABASE = 'sqlite:///db.sqlite3'

Engine = create_engine(
  DATABASE,
  echo=True
)

session = Session(
  autocommit = False,
  autoflush = True,
  bind = Engine
)