from flask import *
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = os.getenv("SECRET")
db = SQLAlchemy(app)

@app.route("/",methods=["GET"])
def home():
    return render_template("general/home.html")

@app.route("/announcements",methods=["GET"])
def announcements():
    return render_template("general/announcements.html")

from .auth import auth
from .manager import manager
from .student import student
from .teacher import teacher
app.register_blueprint(auth,url_prefix="/auth")
app.register_blueprint(manager,url_prefix="/manager")
app.register_blueprint(student,url_prefix="/student")
app.register_blueprint(teacher,url_prefix="/teacher")