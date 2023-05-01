from sqlalchemy import Column, String, TIMESTAMP, Integer
from sqlalchemy.sql import func
from relational.tables.base import Base

class Message(Base):
    __tablename__ = 'messages'
    id = Column('id', String(36), primary_key=True)
    role = Column('role', Integer, nullable=False)
    text = Column('text', String(1000), nullable=False)
    created_at = Column("created_at", TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp(), nullable=False)
