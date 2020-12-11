from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Boolean, Table, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import simplejson
Base = declarative_base()

association_table = Table('course_student_relation', Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True),
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True)
)
class Serialise(object):
    def _asdict(self):
        result = simplejson.OrderedDict()
        for key in self.__mapper__.c.keys():
            if isinstance(getattr(self, key), datetime):
                result["x"] = getattr(self, key).timestamp() * 1000
                result["timestamp"] = result["x"]
            else:
                result[key] = getattr(self, key)

        return result

class Course(Base, Serialise):
    def __init__(self,authorId):
        self.authorId = authorId
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    authorId = Column(Integer, ForeignKey('professors.id'))
    students = relationship("Student", secondary = association_table, back_populates="courses")

class Professor(Base, Serialise):
    def __init__(self, owner):
        self.owner = owner
    __tablename__ = 'professors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner = Column(String, ForeignKey('users.username'))
    courses = relationship("Course")

class Student(Base, Serialise):
    def __init__(self, owner):
        self.owner = owner
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner = Column(String, ForeignKey('users.username'))
    courses = relationship("Course", secondary = association_table, back_populates="students")

class User(Base, Serialise):
    def __init__(self, username, password):
        self.username = username
        self.password = password
    __tablename__ = 'users'
    username = Column(String, primary_key = True)
    password = Column(String)

class Request(Base, Serialise):
    def __init__(self, courseId, studentId):
        self.studentId = studentId
        self.courseId = courseId
        self.status = False
    __tablename__ = 'requests'
    studentId = Column(Integer, ForeignKey('students.id'), primary_key=True)
    courseId = Column(Integer, ForeignKey('courses.id'), primary_key=True)
    status = Column(Boolean)

