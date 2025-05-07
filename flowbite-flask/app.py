from flask import Flask, render_template, redirect, flash
from flask import request
from data.teachers import Teacher
from data.students import Student
from data.portfolios import Portfolio
from data.classes import Classroom
from forms.login import LoginForm, RegisterForm, AddNewCLass, AddNewStudent, AddNewPortfolio
import os
from data.db_init import db


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../db/database_pk.db"

db.init_app(app)

with app.app_context():
    db.create_all()

current_user: Teacher | Student | None = None
user_type = None


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/teacher-login", methods=['POST', 'GET'])
def teacher_log():
    global current_user, user_type
    form = LoginForm()
    if form.validate_on_submit():
        teacher = db.session.query(Teacher).filter(Teacher.login == form.login.data).first()
        if teacher and teacher.check_password(form.password.data):
            current_user = teacher
            user_type = "teacher"
            return redirect('/teacher-acc')
        else:
            print('Неверный логин или пароль')
            return redirect('/teacher-login')
    return render_template("teacher-login.html", form=form)


@app.route("/student-login", methods=['POST', 'GET'])
def student_log():
    global current_user, user_type
    form = LoginForm()
    if form.validate_on_submit():
        student = db.session.query(Student).filter(Student.login == form.login.data).first()
        if student and student.check_password(form.password.data):
            current_user = student
            user_type = "student"
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


@app.route("/teacher-acc")
def teacher_acc():
    if not (current_user and user_type == "teacher"):
        return redirect("/teacher-login")
    return render_template("teacher-acc.html", teacher=current_user,
                           classes=[c for c in db.session.query(Classroom).all() if c.teacher_id == current_user.id])


@app.route("/student-acc")
def student_acc():
    if not (current_user and user_type == "student"):
        return redirect("/student-login")
    portfolios = [p for p in db.session.query(Portfolio).all() if p.student_id == current_user.id]
    classroom = [c for c in db.session.query(Classroom).all() if c.id == current_user.class_id][0]
    form = AddNewPortfolio()
    if form.validate_on_submit():
        port = Portfolio(
            name=form.name.data,
            subject=form.subject.data,
            level=form.level.data,
            result=form.result.data,
            file=form.file.data
        )
        db.session.add(port)
        db.session.commit()
    return render_template("student-acc.html", student=current_user, class_name=classroom.class_number,
                           portfolio=portfolios, form=form)


@app.route("/student-acc-show/<int:id>/<login>/<name>")
def student_acc_show(id, login, name):
    portfolios = [p for p in db.session.query(Portfolio).all() if p.student_id == id]
    return render_template("student-acc-show.html", student_id=id, portfolios=portfolios, login=login, name=name)


@app.route("/add-class/<int:id>", methods=['GET', 'POST'])
def new_class(id):
    form = AddNewCLass()
    if form.validate_on_submit():
        if db.session.query(Classroom).filter(Classroom.class_number == form.name.data).first():
            return render_template('add-class.html', title='Создание класса',
                                   form=form,
                                   message="Такой класс уже есть")
        classroom = Classroom(
            class_number=form.name.data,
            teacher_id=id,
        )
        db.session.add(classroom)
        db.session.commit()
        return redirect('/teacher-acc')
    return render_template('add-class.html', title='Создание класса', form=form)


@app.route("/teacher-acc-class/<int:classroom>/<classroom_name>")
def teacher_acc_class(classroom, classroom_name):
    if not (current_user and user_type == "teacher"):
        return redirect("/teacher-login")
    students = [s for s in db.session.query(Student).all() if s.class_id == classroom]
    print(students)
    return render_template("teacher-acc-class.html", teacher=current_user, students=students,
                           c_id=classroom, classroom_name=classroom_name)


@app.route("/add-student/<int:id>/<name>", methods=['GET', 'POST'])
def new_student(id, name):
    form = AddNewStudent()
    if form.validate_on_submit():
        if db.session.query(Student).filter(Student.login == form.login.data).first():
            return render_template('add-student.html', title='Добавление ученика',
                                   form=form,
                                   message="Такой ученик уже есть")
        student = Student(
            login=form.login.data,
            name=form.name.data,
            class_id=id
        )
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        return redirect(f'/teacher-acc-class/{id}/{name}')
    return render_template('add-student.html', title='Создание класса', form=form)


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
