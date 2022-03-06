from . import db

student_course = db.Table('student_course',
    db.Column('student_id' ,db.Integer,db.ForeignKey('student.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30),nullable = False)
    password = db.Column(db.String(80),nullable = False)
    name = db.Column(db.String(60),nullable = False)
    role = db.Column(db.Integer,nullable = False)
    info_s = db.relationship('Student', backref='user', uselist=False)
    info_t = db.relationship('Teacher', backref='user', uselist=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    phone = db.Column(db.String(12),nullable = False)
    email = db.Column(db.String(250),nullable = False)
    grade = db.Column(db.Integer, nullable = False)
    major = db.Column(db.Integer,db.ForeignKey('student_major.id'))
    debt = db.Column(db.Integer, nullable = False)
    scores = db.relationship('Test_score',backref='student', uselist=False)
    courses = db.relationship('Course', secondary = student_course, backref='students')

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    phone = db.Column(db.String(12),nullable = False)
    email = db.Column(db.String(250),nullable = False)
    major = db.Column(db.Integer,db.ForeignKey('teacher_major.id'))
    detail = db.Column(db.Text, nullable = False)
    courses = db.relationship('Course', backref='teacher')
        
class Course(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    grade = db.Column(db.Integer,nullable = False)
    title = db.Column(db.String(60),nullable = False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    fee = db.Column(db.Integer,nullable = False)
    day = db.Column(db.Integer,nullable = False)
    time = db.Column(db.Time,nullable = False)
    available = db.Column(db.Boolean,nullable = False)
    link = db.Column(db.String(250))
    exams = db.relationship('Exam', backref='course')

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    title = db.Column(db.String(60))
    date = db.Column(db.DateTime)
    number_of_questions = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    max_score = db.Column(db.Integer)
    questions = db.relationship('Question', backref="exam")
    scores = db.relationship('Test_score', backref="exam")

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    exam_id = db.Column(db.Integer,db.ForeignKey('exam.id'))
    order = db.Column(db.Integer)
    body = db.Column(db.Text,nullable = False)
    option_1 = db.Column(db.Text,nullable = False)
    option_2 = db.Column(db.Text,nullable = False)
    option_3 = db.Column(db.Text,nullable = False)
    option_4 = db.Column(db.Text,nullable = False)
    answer = db.Column(db.Integer,nullable = False)

class Test_score(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    exam_id = db.Column(db.Integer,db.ForeignKey('exam.id'))
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'))
    score = db.Column(db.Float,nullable = False)


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    message = db.Column(db.Text,nullable = False)
    date = db.Column(db.DateTime,nullable = False)
    email = db.Column(db.String(120), nullable = False)
    def __init__(self,message,date):
        self.message = message
        self.date = date
        
class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sender = db.Column(db.Integer)
    receiver = db.Column(db.Integer)
    body = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable = False)

class Teacher_major(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    people = db.relationship('Teacher', backref='teacher_major')

class Student_major(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    people = db.relationship('Student', backref='student_major')

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    date_time = db.Column(db.DateTime)


