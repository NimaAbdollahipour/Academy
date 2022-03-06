from flask import *
from . import db
from .models import *
import datetime
teacher = Blueprint('teacher',__name__)

@teacher.route('/',methods=["GET"])
def dashboard():
    if session.get('name'):
        c_s = Course.query.filter_by(teacher_id = session.get('id')).all()
        return render_template('teacher/dashboard.html', courses=c_s,name=session.get('name'))
    else:
        return redirect('auth.login')

@teacher.route('/course',methods=['GET'])
def course():
    if session.get('name'):
        if request.args.get('id'):
            session['course']= request.args.get('id')
            c = Course.query.get(request.args.get('id'))
            e_s = Exam.query.filter_by(course_id=c.id)
            return render_template('teacher/course.html',course = c,exams=e_s)
        else:
            c = Course.query.get(session['course'])
            e_s = Exam.query.filter_by(course_id=c.id)
            return render_template('teacher/course.html',course = c,exams=e_s)
    else:
        return redirect(url_for('auth.login'))


@teacher.route('/exam',methods=['GET','POST'])
def exam():
    if session.get('name'):
        if request.method == 'GET':
            return render_template('teacher/exam.html')
        else:
            for key,value in request.form.items():
                if not value or value=='':
                    flash('Missing '+key+'!')
                    return redirect(url_for('teacher.exam'))
            e = Exam(
                course_id = session.get('course'),
                title = request.form.get('title'),
                date = datetime.datetime(
                    int(request.form.get('date').split('-')[0]),
                    int(request.form.get('date').split('-')[1]),
                    int(request.form.get('date').split('-')[2]),
                    int(request.form.get('time').split(':')[0]),
                    int(request.form.get('time').split(':')[1])),
                number_of_questions = request.form.get('number_of_questions'),
                duration = request.form.get('duration'),
                max_score = request.form.get('max_score')
            )
            db.session.add(e)
            db.session.commit()
            flash('Added Exam Successfully!')
            session['nq'] = int(request.form.get('number_of_questions'))
            session['q'] = 1
            session['exam'] = e.id
            return redirect(url_for('teacher.question'))
    else:
        return redirect(url_for('auth.login'))

@teacher.route('/question',methods=['GET','POST'])
def question():
    if session.get('name'):
        if request.method == 'GET':
            if session.get('q') <= session.get('nq'):
                return render_template('teacher/question.html')
            else:
                flash('All Questions Saved!')
                return redirect(url_for('teacher.question'))
        else:
            for key,value in request.form.items():
                if not value:
                    flash('Missing '+key+' !')
                    return redirect(url_for('teacher.question'))
            q = Question(
                exam_id = session.get('exam'),
                order = session.get('q'),
                body = request.form.get('body'),
                option_1 = request.form.get('option1'),
                option_2 = request.form.get('option2'),
                option_3 = request.form.get('option3'),
                option_4 = request.form.get('option4'),
                answer = request.form.get('answer')
            )
            db.session.add(q)
            db.session.commit()
            flash('Question '+str(session.get('q'))+' Saved Successfully!')
            session['q'] = session.get('q')+1
            if session.get('q') > session.get('nq'):
                flash('All Question Saved!')
                return redirect(url_for('teacher.exam'))
            return redirect(url_for('teacher.question'))
    else:
        return redirect(url_for('auth.login'))

@teacher.route('/scores',methods=['GET'])
def scores():
    if session.get('name'):
        e_i = request.args.get('exam_id')
        scs = Test_score.query.filter_by(exam_id=e_i)
        scs_list = []
        for i in scs:
            scs_list.append((i,User.query.get(i.student_id)))
        return render_template('teacher/scores.html', scores=scs_list)
    else:
        return redirect(url_for('auth.login'))