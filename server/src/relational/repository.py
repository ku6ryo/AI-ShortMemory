from relational.schema import session
from relational.tables.message import Message
from relational.tables.summary import Summary
import uuid
from sqlalchemy import desc

class Repository():

  def __init__(self):
    pass

  def addMessage(self, session_id: str, role: int, text: str):
    m = Message()
    m.id = str(uuid.uuid4())
    m.session_id = session_id
    m.role = role
    m.text = text
    session.add(m)
    session.commit()
    return m.id
  
  def getMessages(self, session_id: str, limit = 100):
    messages = session.query(Message) \
        .where(Message.session_id == session_id) \
        .order_by(desc("created_at")).limit(limit).all()
    return messages

  def addSummary(self, session_id: str, text: str):
    s = Summary()
    s.id = str(uuid.uuid4())
    s.session_id = session_id
    s.text = text
    session.add(s)
    session.commit()
    return s.id

  def getSummaries(self, ids: list):
    return session.query(Summary).filter(Summary.id.in_(ids)).all()