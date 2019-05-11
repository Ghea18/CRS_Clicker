from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user = Column(String(50))
    name = Column(String(128))
    mail = Column(String(128))
    password = Column(String(128))
    rank = Column(String(50))
    date = Column(DateTime, default=datetime.utcnow)
    stat = Column(String(120))

    def __init__(self, user=None, name=None, mail=None, password=None, rank=None, date=None, stat=None):
        self.user = user
        self.name = name
        self.mail = mail
        self.password = password
        self.rank = rank
        self.date = date
        self.stat = stat

    def __repr__(self):
        return '<user %r>' % (self.user)

class Score(Base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True)
    quiz_id = Column(String(50))
    answer = Column(String(50))
    key = Column(String(50))
    stat = Column(Integer, default=0)
    date = Column(DateTime, default=datetime.utcnow)

    def __init__(self, quiz_id=None, answer=None, key=None, stat=None, date=None):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.date = date
        self.stat = stat

    def __repr__(self):
        return '<score %r>' % (self.score)
