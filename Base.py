

from sqlalchemy import Column, Integer, ForeignKey, Boolean, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    authorId = Column(Integer, ForeignKey('professors.id'))
    students = relationship("StudentAndCourse")

class Professor(Base):
    __tablename__ = 'professors'
    id = Column(Integer, primary_key=True)
    courses = relationship("Course")

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    courses = relationship("StudentAndCourse")

class Request(Base):
    __tablename__ = 'requests'
    studentId = Column(Integer, ForeignKey('students.id'))
    courseId = Column(Integer, ForeignKey('courses.id'))
    status = Column(Boolean)
    __table_args__ = (
        PrimaryKeyConstraint('studentId', 'courseId'),
        {},
    )

class StudentAndCourse(Base):
    __tablename__ = 'studentsAndCourses'
    studentId = Column(Integer, ForeignKey('students.id'))
    courseId = Column(Integer, ForeignKey('courses.id'))
    __table_args__ = (
        PrimaryKeyConstraint('studentId', 'courseId'),
        {},
    )

