from sqlalchemy.orm import Session
from relational.tables.message import Message
from relational.create_engine import create_engine

engine = create_engine()

session = Session(
  autocommit = False,
  autoflush = True,
  bind = engine
)