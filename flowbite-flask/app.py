from flask import Flask, render_template, redirect
from flask import request
from data import db_session
from data.teachers import Teacher
from forms.teacher_log import LoginForm
import os
SECRET_KEY = os.urandom(32)


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/teacher-login", methods=['POST', 'GET'])
def t_log():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/teacher-acc')
    return render_template("teacher-login.html")


@app.route("/student-login", methods=['POST', 'GET'])
def s_log():
    if request.method == 'GET':
        return render_template("student-login.html")
    elif request.method == 'POST':
        return request.form['login'], request.form['password']


@app.route("/teacher-acc")
def t_acc():
    return render_template("teacher-acc.html")


@app.route("/student-acc")
def s_acc():
    return render_template("student-acc.html")


if __name__ == '__main__':
    # db_session.global_init("flowbite-flask/pk_database1.db")
    # teacher = Teacher()
    # teacher.name = "Марья Ивановна"
    # teacher.login = "pk_mary_ivanovna"
    # teacher.password = "456"
    # db_sess = db_session.create_session()
    # db_sess.add(teacher)
    # db_sess.commit()
    app.run(host="127.0.0.1", port=8080, debug=True)
