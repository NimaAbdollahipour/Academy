from academy.models import *
from academy import db
db.create_all()
db.session.add(User(name='nima',role=1,password='nima',username='nima'))
db.session.add(Teacher_major(name='Math'))
db.session.add(Teacher_major(name='Biology'))
db.session.add(Teacher_major(name='Physics'))
db.session.add(Teacher_major(name='Chemistery'))
db.session.add(Student_major(name='Math'))
db.session.add(Student_major(name='Science'))
db.session.commit()
