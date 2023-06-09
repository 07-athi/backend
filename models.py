from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
 
db = SQLAlchemy()
 
def get_uuid():
    return uuid4().hex
 
class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, unique=True, default=get_uuid)
    name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, unique=True, primary_key=True)
    role = db.Column(db.Text, nullable=False)
    classid = db.Column(db.Text, nullable=False)
    rollid = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)

class Teacher(db.Model):
    __tablename__ = "teacher"
    __table_args__ = {'extend_existing': True}
    teacherid = db.Column(db.Text, nullable=False, unique=True)
    teachername = db.Column(db.Text, nullable=False)
    tmail = db.Column(db.Text, unique=True, primary_key=True)
    classid = db.Column(db.Text, nullable=False)

class Student(db.Model):
    __tablename__ = "student"
    __table_args__ = {'extend_existing': True}
    studentrollno = db.Column(db.Text, nullable=False, unique=True)
    classid = db.Column(db.Text, nullable=False)
    stuname = db.Column(db.Text, nullable=False)
    stumail = db.Column(db.Text, unique=True, primary_key=True)


