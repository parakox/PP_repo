
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
import hashlib
from Base import Professor,Student,Course,Request,User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine("postgresql://root:example@localhost:5432/pp")
Session = sessionmaker(bind=engine)
session = Session()
auth = HTTPBasicAuth()
app = Flask(__name__)

@app.route('/api/v1/hello-world-28', methods = ['GET'])
def hello():
    return "Hello World 28"

@app.route('/register', methods = ['POST'])
def register():
    data = request.get_json()
    try:
        username = data['username']
        password = data['password']
        if session.query(User).filter_by(username = username).first() is None:
            session.add(User(username, hashlib.md5(password.encode()).hexdigest()))
            session.commit()
            return 'Successful', 200
        else:
            return 'Username is already in use', 200
    except:
        return 'Invalid input', 404

@auth.verify_password
def verify_password(username, password):
    return session.query(User).filter_by(username = username, password = hashlib.md5(password.encode()).hexdigest()).first() is not None

@app.route('/professors/<professorId>', methods = ['GET'])
@auth.login_required
def getProfessor(professorId):
        professor = session.query(Professor).filter_by(id = int(professorId)).first()
        if professor is None:
            return "Professor not found", 404
        courses = []
        for course in professor.courses:
            courses.append(course._asdict())
        return jsonify(id = professor.id,owner = professor.owner,courses =professor.courses), 200

@app.route('/add_course', methods = ['POST'])
@auth.login_required
def addCourse():
    professor = session.query(Professor).filter_by(owner = auth.current_user()).first()
    if professor is None:
        return 'You are not professor', 405
    session.add(Course(professor.id))
    session.commit()
    return "Successful", 200

@app.route('/delete_course/<id>', methods = ['POST'])
@auth.login_required
def deleteCourse(id):
    try:
        professor = session.query(Professor).filter_by(owner = auth.current_user()).first()
        if professor is None:
            return 'You are not professor', 405
        for course in professor.courses:
            if course.id == int(id):
                session.delete(course)
                session.commit()
                return 'Successful', 200
        return 'Course doesn\'t belong to professor'
    except:
        return 'Invalid ID supplied', 400

@app.route('/add_professor', methods = ['POST'])
@auth.login_required
def addProfessor():
    if session.query(Professor).filter_by(owner=auth.current_user()).first() is None:
        session.add(Professor(auth.current_user()))
        session.commit()
        return "Successful", 200
    return "User is already professor", 404

@app.route('/add_student', methods = ['POST'])
@auth.login_required
def addStudent():
    if session.query(Student).filter_by(owner=auth.current_user()).first() is None:
        session.add(Student(auth.current_user()))
        session.commit()
        return "Successful", 200
    return "User is already student", 404

@app.route('/my_courses', methods = ['GET'])
@auth.login_required
def getMyCourses():
    professor = session.query(Professor).filter_by(owner=auth.current_user()).first()
    if professor is not None:
        courses = []
        for course in professor.courses:
            courses.append(course._asdict())
        return jsonify(courses = courses), 200
    return 'Courses not found', 404

@app.route('/my_available_courses', methods = ['GET'])
@auth.login_required
def getMyAvailableCourses():
    student = session.query(Student).filter_by(owner=auth.current_user()).first()
    if student is not None:
        courses = []
        for course in student.courses:
            courses.append(course._asdict())
        return jsonify(courses=courses), 200
    return 'Courses not found', 404

@app.route('/request_course/<courseId>', methods = ['POST'])
@auth.login_required
def requestCourse(courseId):
    try:
        courseId = int(courseId)
    except:
        return 'Invalid ID supplied', 400
    student = session.query(Student).filter_by(owner=auth.current_user()).first()
    if student is None:
        return 'You are not student', 404
    course = session.query(Course).filter_by(id = courseId).first()
    if course is None:
        return 'No course found', 403
    if session.query(Request).filter_by(studentId = student.id, courseId = course.id).first() is not None:
        return 'You already created request', 402
    session.add(Request(course.id,student.id))
    session.commit()
    return 'Successful', 200

@app.route('/accept_request/<courseId>/<studentId>', methods = ['POST'])
@auth.login_required
def acceptRequest(courseId, studentId):
    try:
        studentId = int(studentId)
        courseId = int(courseId)
    except:
        return 'Invalid path variables', 406
    request =  session.query(Request).filter_by(courseId = courseId, studentId = studentId).first()
    if request is None:
        return 'No such request', 405
    if request.status:
        return 'Request was already accepted', 404
    student = session.query(Student).filter_by(id = studentId).first()
    if student is None:
        return 'Student no longer exists', 403
    professor = session.query(Professor).filter_by(owner = auth.current_user()).first()
    if professor is None:
        return 'You are not professor', 402
    for course in professor.courses:
        if course.id == courseId:
            if len(course.students) >= 5:
                return 'Course has max amount of students', 401
            course.students.append(student)
            request.status = True
            session.commit()
            return 'Successful', 200
    return 'Course doesn\'t belong to professor', 400

@app.route('/courses/<courseId>', methods = ['GET'])
@auth.login_required
def getCourse(courseId):
    try:
        courseId = int(courseId)
    except:
        return 'Invalid ID supplied', 404
    professor = session.query(Professor).filter_by(owner = auth.current_user()).first()
    if professor is not None:
        for course in professor.courses:
            if course.id == courseId:
                students = []
                for studentt in course.students:
                    students.append(studentt._asdict())
                return jsonify(id=course.id, authorId=course.authorId, students=students), 200
    student = session.query(Student).filter_by(owner = auth.current_user()).first()
    if student is not None:
        for course in student.courses:
            if course.id == courseId:
                students= []
                for studentt in course.students:
                    students.append(studentt._asdict())
                return jsonify(id = course.id, authorId = course.authorId, students = students), 200
    return 'No access to course', 403

if __name__ == '__main__':
    app.run()
