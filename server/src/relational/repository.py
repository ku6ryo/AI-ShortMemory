from relational.schema import session
from relational.tables.message import Message
import uuid
from sqlalchemy import desc

class Repository():

  def __init__(self):
    pass

  def add(self, session_id: str, role: int, text: str):
    m = Message()
    m.id = str(uuid.uuid4())
    m.session_id = session_id
    m.role = role
    m.text = text
    session.add(m)
    session.commit()
    return m.id
  
  def remove(self, id):
    m = session.query(Message).filter(Message.id == id).first()
    session.delete(m)
    session.commit()
  
  def getMessages(self, session_id: str, limit = 100):
    messages = session.query(Message) \
        .where(Message.session_id == session_id) \
        .order_by(desc("created_at")).limit(limit).all()
    return messages