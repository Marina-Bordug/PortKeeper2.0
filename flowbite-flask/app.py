from flask import Flask, render_template, redirect, flash
from flask import request
from flask_login import LoginManager, current_user, login_user, login_required
from data.teachers import Teacher
from data.students import Student
from data.portfolios import Portfolio
from data.classes import Classroom
from forms.login import LoginForm, RegisterForm
import os
from data.db_init import db


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = os.urandom(32)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../db/database_pk.db"

db.init_app(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Teacher).filter(Teacher.id == user_id).first()


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/teacher-login", methods=['POST', 'GET'])
def teacher_log():
    form = LoginForm()
    if form.validate_on_submit():
        teacher = db.session.query(Teacher).filter(Teacher.login == form.login.data).first()
        if teacher and teacher.check_password(form.password.data):
            login_user(teacher)
            return redirect('/teacher-acc')
        else:
            print('Неверный логин или пароль')
            return redirect('/teacher-login')
    return render_template("teacher-login.html", form=form)


@app.route("/student-login", methods=['POST', 'GET'])
def student_log():
    form = LoginForm()
    if form.validate_on_submit():
        student = db.session.query(Student).filter(Student.login == form.login.data).first()
        if student and student.check_password(form.password.data):
            login_user(student)
            return redirect('/student-acc')
        else:
            print('Неверный логин или пароль')
            return redirect('/student-login')
    return render_template("student-login.html", form=form)


@app.route("/create-acc", methods=['GET', 'POST'])
def new_acc():
    form = RegisterForm()
    if form.validate_on_submit():
        if db.session.query(Teacher).filter(Teacher.login == form.login.data).first():
            return render_template('create-acc.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        teacher = Teacher(
            name=form.name.data,
            login=form.login.data,
        )
        teacher.set_password(form.password.data)
        db.session.add(teacher)
        db.session.commit()
        return redirect('/teacher-login')
    return render_template('create-acc.html', title='Регистрация', form=form)


@login_required
@app.route("/teacher-acc")
def teacher_acc():
    teacher = db.session.query(Teacher).filter(Teacher.id == current_user.id).first()
    classes = [c for c in db.session.query(Classroom).all() if c.teacher_id == teacher.id]
    return render_template("teacher-acc.html", teacher=teacher, classes=classes)


@login_required
@app.route("/student-acc")
def student_acc():
    students = db.session.query(Student)
    return render_template("student-acc.html", students=students)


if __name__ == '__main__':
    # db_session.global_init("./flowbite-flask/pk_database1.db")
    # teacher = Teacher()
    # teacher.name = "Марья Ивановна"
    # teacher.login = "pk_mary_ivanovna"
    # teacher.password = "456"
    # db_sess = db_session.create_session()
    # db_sess.add(teacher)
    # db_sess.commit()
    app.run(host="127.0.0.1", port=8082, debug=True)
