from flask import *
from . import db
from .models import *
import datetime
student = Blueprint('student',__name__)

@student.route('/',methods=["GET"])
def dashboard():
    if session.get('name'):
        c_s = User.query.get(session.get('id'))
        return render_template('student/dashboard.html', courses=c_s.info_s.courses,name=session.get('name'))
    else:
        return redirect(url_for('auth.login'))

@student.route('/course',methods=["GET"])
def course():
    if session.get('name'):
        id=request.args.get('id')
        if id:
            c=Course.query.get(id)
            session['course'] = id
        else:
            c=Course.query.get(session.get('course'))
        return render_template('student/course.html',course=c,exams=c.exams)
    else:
        return redirect(url_for('auth.login'))

@student.route('/exam',methods=["GET","POST"])
def exam():
    if session.get('name'):
        if request.method == 'GET':
            id = request.args.get('id')
            if id:
                e=Exam.query.get(id)
                session['exam'] = id
                session['score'] = 0
            else:
                e=Exam.query.get(session.get('exam'))
            s = ''
            a = False
            if datetime.datetime.now() > e.date and datetime.datetime.now() < e.date + datetime.timedelta(minutes=e.duration):
                a = True
            for i in e.scores:
                if i.student_id == session.get('id'):
                    a = False
            else:
                s_list = e.scores
                if s_list:
                    for i in s_list:
                        if i.student_id == session.get('id'):
                            s = i.score
            return render_template('student/exam.html',exam=e, available=a, score=s)
    else:
        return redirect(url_for('auth.login'))

@student.route('/question',methods=["GET","POST"])
def question():
    if session.get('name'):
        if request.method == 'GET':
            q = request.args.get('q')
            if q:
                e = Exam.query.get(session.get('exam'))
                if int(q) > e.number_of_questions:
                    flash('Your Score: '+str(session.get('score')))
                    flash('You finished the exam!')
                    tts = Test_score(student_id=session.get('id'),exam_id=session.get('exam'),score=session.get('score'))
                    db.session.add(tts)
                    db.session.commit()
                    session.pop('exam')
                    session.pop('score')
                    session.pop('order')
                    return redirect(url_for('student.course'))

                if not session.get('order') or int(q)>=int(session.get('order')):
                    session['order'] = q
                    req_question = e.questions[int(q)-1]
                    return render_template('student/question.html',question=req_question)
                else:
                    flash('You are not allowed to see this question!')
                    return redirect(url_for('student.dashboard'))
            else:
                return redirect(url_for('student.dashboard'))
        else:
            q = session.get('order')
            op = request.form.get('option')
            e = Exam.query.get(session.get('exam'))
            question = e.questions[int(q)-1]
            if int(op) == int(question.answer):
                if session.get('score'):
                    session['score']+=1
                else:
                    session['score'] = 1
                    print(url_for('student.question')+'?q='+str(int(q)+1))
            return redirect(url_for('student.question')+'?q='+str(int(q)+1))

    else:
        return redirect(url_for('auth.login'))