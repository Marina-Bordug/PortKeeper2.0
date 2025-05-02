from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()], render_kw={"placeholder": "Логин"})
    password = PasswordField('Пароль', validators=[DataRequired(), Length(3, 10)], render_kw={"placeholder": "Пароль"})
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(3, 10)], render_kw={"placeholder": "Пароль"})
    submit = SubmitField('Войти')


class AddNewCLass(FlaskForm):
    name = StringField('Имя класса', validators=[DataRequired()])
    submit = SubmitField('Создать')


class AddNewStudent(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(3, 10)], render_kw={"placeholder": "Пароль"})
    submit = SubmitField('Добавить')