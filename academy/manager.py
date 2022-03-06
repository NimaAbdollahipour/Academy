from flask import *
from . import db
from .models import *
import datetime
manager = Blueprint('manager',__name__)

@manager.route('/',methods=["GET"])
def dashboard():
    name = session.get('name')
    if name:
        return render_template('manager/dashboard.html',name=session.get('name'))
    else:
        return redirect(url_for('auth.login'))


@manager.route('/teacher',methods=['POST','GET'])
def teacher():
    name = session.get('name')
    m = Teacher_major.query.all()
    t = User.query.filter_by(role=2).all()
    t_list=[]
    for i in t:
        t_list.append((i,Teacher_major.query.get(i.info_t.major)))
    if name:
        if request.method == 'GET':
            return render_template('manager/teacher.html',teachers=t_list,majors=m)
        else:
            for key,value in request.form.items():
                if not value or value=='':
                    flash('Missing ',key,'!')
                    return redirect(url_for('manager.teacher'))
            if User.query.filter_by(username = request.form.get('username')).first():
                flash('Teacher with this username already exists!')
                return redirect(url_for('manager.teacher'))
            else:
                new_user = User(
                    name=request.form.get('name'),
                    username=request.form.get('username'),
                    password=request.form.get('password'),
                    role=2
                )
                db.session.add(new_user)
                db.session.commit()
                db.session.add(Teacher(
                    user_id = new_user.id,
                    phone =request.form.get('phone'),
                    email=request.form.get('email'),
                    major=request.form.get('major'),
                    detail=request.form.get('detail') 
                    ))
                db.session.commit()
                return redirect(url_for('manager.teacher'))
    else:
        return redirect(url_for('auth.login'))


@manager.route('/student',methods=['GET','POST'])
def student():
    m = Student_major.query.all()
    s = User.query.filter_by(role=3).all()
    s_list=[]
    for i in s:
        s_list.append((i,Student_major.query.get(i.info_s.major)))
    if session.get('name'):
        if request.method == 'GET':
            return render_template('manager/student.html',students=s_list,majors=m)
        else:
            for key,value in request.form.items():
                if not value or value=='':
                    flash('Missing '+key+'!')
                    return redirect(url_for('manager.student'))
            if User.query.filter_by(username = request.form.get('username')).first():
                flash('Student with this username already exists!')
                return redirect(url_for('manager.student'))
            else:
                new_user = User(
                    name=request.form.get('name'),
                    username=request.form.get('username'),
                    password=request.form.get('password'),
                    role=3
                )
                db.session.add(new_user)
                db.session.commit()
                db.session.add(Student(
                    user_id = new_user.id,
                    phone =request.form.get('phone'),
                    email=request.form.get('email'),
                    major=request.form.get('major'),
                    grade = request.form.get('grade'),
                    debt = 0
                    ))
                db.session.commit()
                return redirect(url_for('manager.student'))
    else:
        return redirect(url_for('auth.login'))


@manager.route('/course',methods=['GET','POST'])
def course():
    name = session.get('name')
    if name:
        if request.method == 'GET':
            t = User.query.filter_by(role=2).all()
            t_list=[]
            for i in t:
                t_list.append((i,Teacher_major.query.get(i.info_t.major).name))
            cs = Course.query.all()
            cs_list=[]
            days = ['','Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday']
            grades = ['','First Grade','Second Grade','Third Grade']
            for i in cs:
                cs_list.append((i,days[i.day],grades[i.grade],User.query.get(i.teacher_id)))
            return render_template('manager/course.html',teachers=t_list,courses=cs_list)
        else:
            for key,value in request.form.items():
                if not value or value=='':
                    flash('Missing '+key+' !')
                    return redirect(url_for('manager.course'))
            form_title = request.form.get('title')
            form_fee = request.form.get('fee')
            form_time = datetime.time(int(request.form.get('time').split(':')[0]),int(request.form.get('time').split(':')[1]))
            form_av = None
            if request.form.get('available'):
                form_av=True
            else:
                form_av=False
            form_teacher_id = request.form.get('teacher_id')
            form_day = request.form.get('day')
            form_grade = request.form.get('grade')
            form_link = request.form.get('link')
            
            new_course = Course(
                title = form_title,
                fee = form_fee,
                time = form_time,
                available = form_av,
                teacher_id = form_teacher_id,
                day = form_day,
                grade = form_grade,
                link = form_link
            )
            db.session.add(new_course)
            db.session.commit()
            flash('Course added successfully!')
            return redirect(url_for('manager.course'))
            
    else:
        return redirect(url_for('auth.login'))



@manager.route('/announcement',methods=['GET','POST'])
def announcement():
    if session.get('name'):
        if request.method == 'GET':
            a_s = Announcement.query.all()
            return render_template('manager/announcement.html',announcements = a_s)
        else:
            for key,value in request.form.items():
                if not value or value=='':
                    flash('Missing '+key+'!')
                    return redirect(url_for('manager.announcement'))
            form_title = request.form.get('title')
            form_body = request.form.get('body')
            a = Announcement(
                title = form_title,
                body = form_body,
                date_time = datetime.datetime.now() 
            )
            db.session.add(a)
            db.session.commit()
            flash('Added Successfully!')
            return redirect(url_for('manager.announcement'))
    else:
        return redirect(url_for('auth.login'))


@manager.route('/del_announce',methods=['GET'])
def del_announce():
    if session.get('name'):
        a = Announcement.query.get(request.args.get('id'))
        db.session.delete(a)
        db.session.commit()
        flash('Deleted Successfully!')
        return redirect(url_for("manager.announcement"))
    else:
        return redirect(url_for('auth.login'))


@manager.route('/selectcourse',methods=['GET'])
def select_course():
    if session.get('name'):
        id = request.args.get('id')
        if id:
            session['course'] = id
            std = User.query.filter_by(role=3).all()
            return render_template('manager/student_course.html',students = std)
        else:
            c_s = Course.query.all()
            return render_template('manager/select.html',courses=c_s)
    else:
        return redirect(url_for('auth.login'))


@manager.route('/studentcourse',methods=['POST'])
def course_student():
    if session.get('name'):
        s = request.form.get('student')
        if s:
            current_course = Course.query.get(session.get('course'))
            student = User.query.get(s)
            student.info_s.courses.append(current_course)
            db.session.commit()
        return redirect(url_for('manager.select_course'))
    else:
        return redirect(url_for('auth.login'))