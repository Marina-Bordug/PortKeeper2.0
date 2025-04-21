from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/teacher-login")
def t_log():
    return render_template("teacher-login.html")


@app.route("/student-login")
def s_log():
    return render_template("student-login.html")


@app.route("/teacher-acc")
def t_acc():
    return render_template("teacher-acc.html")


@app.route("/student-acc")
def s_acc():
    return render_template("student-acc.html")


if __name__ == '__main__':
    app.run(debug=True)
