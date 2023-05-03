from sqlalchemy.orm import Session
from relational.create_engine import create_engine
# Import tables to recognize them as ORM classes
from relational.tables.message import Message
from relational.tables.summary import Summary

engine = create_engine()

session = Session(
  autocommit = False,
  autoflush = True,
  bind = engine
)