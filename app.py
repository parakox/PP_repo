from flask import Flask, g, request, make_response
import sqlite3
import os, shutil
app = Flask(__name__)

DATABASE = 'db/database.db'

@app.route('/api/v1/hello-world-28', methods = ['GET'])
def hello():
    return "Hello World 28"

@app.route('/api/v2/register', methods = ['POST'])
def register_professor():
    username = request.args.get('username')
    password = request.args.get('password')
    if username is not None and password is not None and len(get_professor_by_username(username)) == 0 and len(username) > 0 and len(password) > 0:
        create_professor(username,password)
        return "Successfully created"
    return "Username is already in use or either username or password are empty",400

@app.route('/api/v2/login', methods = ['POST'])
def login_professor():
    username = request.args.get('username')
    password = request.args.get('password')
    if username is not None and password is not None and len(get_professor_by_username_and_password(username, password)) > 0:
        resp = make_response()
        resp.set_cookie("username", username)
        return resp
    return "Credentials are incorrect",400

@app.route('/api/v2/course/create', methods=['POST'])
def create_course_api():
    username = request.cookies.get("username")
    title = request.args.get("title")
    if username is not None and title is not None and len(get_professor_by_username(username)) > 0 and len(title) > 0 and len(get_course_by_title(title)) == 0:
        create_course(title, username)
        return "Successfully created"
    return "Couldn't create course",400

@app.route('/api/v2/courses', methods=['GET'])
def get_created_courses_by_professor():
    username = request.cookies.get("username")
    if username is not None and len(get_professor_by_username(username)) > 0:
        return "Your courses\n" + str(get_professor_courses(username))
    return "Couldn't get courses",400

@app.route('/api/v2/course/remove', methods = ['POST'])
def remove_course_api():
    username = request.cookies.get("username")
    title = request.args.get("title")
    if username is not None and title is not None and len(get_professor_by_username(username)) > 0 and len(get_course_by_title(title)) > 0 and get_username_assigned_to_course(title) == username:
        remove_course(title)
        return "Successfully deleted course"
    return "Couldn't delete course",400

@app.route('/api/v2/request/create_request', methods = ['POST'])
def create_request_api():
    surname = request.args.get("surname")
    title = request.args.get("title")
    if surname is not None and title is not None and len(get_student_by_surname(surname)) > 0 and len(get_course_by_title(title)) > 0 and len(get_request(surname,title)) == 0 and len(get_student_on_course(surname, title)) == 0:
        create_request(surname, title)
        return "Successfully created request"
    return "Couldn't create request",400

@app.route('/api/v2/request/accept_request', methods = ['POST'])
def accept_request():
    username = request.cookies.get("username")
    surname = request.args.get("surname")
    title = request.args.get("title")
    if surname is not None and title is not None and len(get_student_by_surname(surname)) > 0 and len(get_course_by_title(title)) > 0 and username is not None and len(get_professor_by_username(username)) > 0 and get_username_assigned_to_course(title) == username and len(get_students_on_course(title)) < 5 and len(get_student_on_course(surname,title)) == 0 and len(get_request(surname,title)) > 0 :
        add_student_to_course(surname, title)
        remove_request(surname,title)
        return "Successfully accepted request"
    return "Couldn't accept request",400

@app.route('/api/v2/request/decline_request', methods = ['POST'])
def decline_request():
    username = request.cookies.get("username")
    surname = request.args.get("surname")
    title = request.args.get("title")
    if surname is not None and title is not None and len(get_student_by_surname(surname)) > 0 and len(get_course_by_title(title)) > 0 and username is not None and len(get_professor_by_username(username)) > 0 and get_username_assigned_to_course(title) == username and len(get_request(surname,title)) > 0 :
        remove_request(surname, title)
        return "Successfully declined request"
    return "Couldn't decline request",400

@app.route('/api/v2/student/create_student', methods = ['POST'])
def create_student_api():
    surname = request.args.get("surname")
    if surname is not None and len(get_student_by_surname(surname)) == 0 and len(surname) > 0:
        create_student(surname)
        return "Successfully created student"
    return "Couldn't create student",400

@app.route('/api/v2/student/get_courses', methods = ['GET'])
def get_courses_for_student_api():
    surname = request.args.get("surname")
    if surname is not None and len(get_student_by_surname(surname)) > 0:
        return "Your courses, student\n" + str(get_courses_for_student(surname))
    return "Couldn't get your courses, student",400

@app.route('/api/v2/student/get_info_about_course', methods =['GET'])
def get_info_about_course_api():
    surname = request.args.get("surname")
    title = request.args.get("title")
    if surname is not None and title is not None and len(get_student_by_surname(surname)) > 0 and len(get_course_by_title(title)) > 0 and len(get_student_on_course(surname,title)) > 0 :
        return "Info about course"
    return "You don't have permission to see this info",400
@app.route('/api/v2/course/change_title_of_course', methods = ['POST'])
def change_title_of_course_api():
    username = request.cookies.get("username")
    title = request.args.get("title")
    new_title = request.args.get("new_title")
    if username is not None and title is not None and new_title is not None and len(get_course_by_title(title)) > 0 and len(get_professor_by_username(username)) > 0 and get_username_assigned_to_course(title) == username:
        change_title_of_course(new_title, title)
        return "Successfully changed title of course"
    return "Couldn't change title of course",400

if __name__ == '__main__':
    app.run()
