from flask import Flask, render_template, redirect, flash
from flask import request
from data.teachers import Teacher
from forms.teacher_log import LoginForm, RegisterForm
import os
from data.db_init import db
SECRET_KEY = os.urandom(32)


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../flowbite-flask/db/database_pk.db"

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/teacher-login", methods=['POST', 'GET'])
def t_log():
    form = LoginForm()
    if form.validate_on_submit():
        print(1)
        teacher = db.session.query(Teacher).filter(Teacher.login == form.login.data).first()
        if teacher and teacher.check_password(form.password.data):
        # if teacher:
            return redirect('/teacher-acc')
        else:
            print('Неверный логин или пароль')
            return redirect('/teacher-login')
    return render_template("teacher-login.html", form=form)


@app.route("/student-login", methods=['POST', 'GET'])
def s_log():
    if request.method == 'GET':
        return render_template("student-login.html")
    elif request.method == 'POST':
        return request.form['login'], request.form['password']


@app.route("/create-acc", methods=['GET', 'POST'])
def new_acc():
    form = RegisterForm()
    if form.validate_on_submit():
        # db_sess = db.session.create_session()
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
def t_acc():
    return render_template("teacher-acc.html")


@app.route("/student-acc")
def s_acc():
    return render_template("student-acc.html")


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
