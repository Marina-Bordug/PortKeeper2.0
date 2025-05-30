from io import BytesIO
import pickle
from flask import Flask, render_template, redirect, send_file
from flask import request
from data.teachers import Teacher
from data.students import Student
from data.portfolios import Portfolio
from data.classes import Classroom
from forms.forms import LoginForm, RegisterForm, AddNewCLass, AddNewStudent, AddNewPortfolio
import os
from data.db_init import db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../flowbite-flask/db/database_pk.db"

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
def teacher_login():
    global current_user, user_type
    form = LoginForm()
    if form.validate_on_submit():
        teacher = db.session.query(Teacher).filter(Teacher.login == form.login.data).first()
        if teacher and teacher.check_password(form.password.data):
            current_user = teacher
            user_type = "teacher"
            return redirect('/teacher-acc')
        form.password.errors.append("Неверный логин или пароль")
    return render_template("teacher-login.html", form=form)


@app.route("/student-login", methods=['POST', 'GET'])
def student_login():
    global current_user, user_type
    form = LoginForm()
    if form.validate_on_submit():
        student = db.session.query(Student).filter(Student.login == form.login.data).first()
        if student and student.check_password(form.password.data):
            current_user = student
            user_type = "student"
            return redirect('/student-acc')
        form.password.errors.append("Неверный логин или пароль")
    return render_template("student-login.html", form=form)


@app.route("/create-acc", methods=['GET', 'POST'])
def create_acc():
    form = RegisterForm()
    if form.validate_on_submit():
        if db.session.query(Teacher).filter(Teacher.login == form.login.data).first():
            form.login.errors.append("Пользователь с таким логином уже есть")
        else:
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


@app.route('/class_delete/<int:id>', methods=['GET', 'POST'])
def class_delete(id):
    classroom = db.session.query(Classroom).filter(Classroom.id == id,
                                                   Classroom.teacher_id == current_user.id).first()
    if classroom:
        db.session.delete(classroom)
        db.session.commit()
    return redirect('/teacher-acc')


@app.route("/student-acc", methods=['GET', 'POST'])
def student_acc():
    if not (current_user and user_type == "student"):
        return redirect("/student-login")
    portfolios = db.session.query(Portfolio).filter(Portfolio.student_id == current_user.id).all()
    form = AddNewPortfolio()
    if form.validate_on_submit():
        port = Portfolio(
            name=form.name.data,
            subject=form.subject.data,
            level=form.level.data,
            result=form.result.data,
            file=pickle.dumps((form.file.data.read(), form.file.data.filename.split(".")[-1])),
            student_id=current_user.id
        )
        db.session.add(port)
        db.session.commit()
        return redirect('/student-acc')
    return render_template("student-acc.html", student=current_user, class_name=db.session.query(Classroom).filter(
        Classroom.id == current_user.class_id).first().class_number,
                           portfolio=portfolios, form=form)


@app.route("/student-acc/download/<int:port_id>", methods=["GET", "POST"])
def download(port_id):
    if not (current_user and user_type == "student"):
        return redirect("/student-login")

    port = db.session.query(Portfolio).filter(Portfolio.id == port_id).first()
    if port and port.student_id == current_user.id:
        filedata = pickle.loads(port.file)
        return send_file(BytesIO(filedata[0]), as_attachment=True,
                         download_name=f"{port.result}_{port.name}_{port.level}_уровень_{port.subject}.{filedata[1]}")
    return redirect("/student-acc")


@app.route('/file/<file_name>')
def file(file_name):
    ib = BytesIO(file_name)
    return send_file(ib, as_attachment=False, mimetype='jpeg/jpg/png/pdf')


@app.route('/avatar')
def avatar():
    ib = BytesIO(current_user.avatar)
    return send_file(ib, as_attachment=False, mimetype='jpg')


@app.route('/send-avatar', methods=["POST"])
def get_send_avatar():
    current_user.avatar = request.data
    db.session.merge(current_user)
    db.session.flush()
    db.session.commit()
    return ""


@app.route("/add-class/<int:id>", methods=['GET', 'POST'])
def add_class(id):
    form = AddNewCLass()
    if form.validate_on_submit():
        if db.session.query(Classroom).filter(Classroom.class_number == form.name.data,
                                              Classroom.teacher_id == current_user.id).first():
            form.name.errors.append("Такой класс уже есть")
        else:
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
def add_student(id, name):
    form = AddNewStudent()
    if form.validate_on_submit():
        if db.session.query(Student).filter(Student.login == form.login.data).first():
            form.login.errors.append("Ученик с таким логином уже есть")
        else:
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
    app.run(host="127.0.0.1", port=8080, debug=True)
