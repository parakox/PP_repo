

from sqlalchemy import Column, Integer, ForeignKey, Boolean, PrimaryKeyConstraint, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

association_table = Table('course_student_relation', Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('student_id', Integer, ForeignKey('students.id'))
)

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    authorId = Column(Integer, ForeignKey('professors.id'))
    students = relationship("Course", secondary = association_table, back_populates="courses")

class Professor(Base):
    __tablename__ = 'professors'
    id = Column(Integer, primary_key=True)
    courses = relationship("Course")

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    courses = relationship("Student", secondary = association_table, back_populates="students")

class Request(Base):
    __tablename__ = 'requests'
    studentId = Column(Integer, ForeignKey('students.id'))
    courseId = Column(Integer, ForeignKey('courses.id'))
    status = Column(Boolean)
    __table_args__ = (
        PrimaryKeyConstraint('studentId', 'courseId'),
        {},
    )


