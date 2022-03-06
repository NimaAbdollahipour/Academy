from flask import *
from . import db
from .models import User
auth = Blueprint('auth',__name__)

@auth.route('/login/',methods=["GET","POST"])
def login():
    if request.method == 'GET':
        return render_template('general/login.html')
    else:
        if not (request.form.get('username') and request.form.get('password')):
            flash('Missing Username or Password!')
            return redirect(url_for('auth.login'))
        else:
            db_user = User.query.filter_by(username=request.form.get('username')).first()
            if db_user:
                if db_user.password == request.form.get('password'):
                    session['id'] = db_user.id
                    session['role'] = db_user.role
                    session['name'] = db_user.name
                    if db_user.role == 1:
                        return redirect(url_for('manager.dashboard'))
                    elif db_user.role == 2:
                        return redirect(url_for('teacher.dashboard'))
                    else:
                        return redirect(url_for('student.dashboard'))
                else:
                    flash('Wrong Password!')
                    return redirect(url_for('auth.login'))
            else:
                flash('User not found!')
                return redirect(url_for('auth.login'))
            

@auth.route('/logout/',methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))