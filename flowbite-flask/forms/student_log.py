from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()], render_kw={"placeholder": "Логин"})
    password = PasswordField('Пароль', validators=[DataRequired(), Length(3, 10)], render_kw={"placeholder": "Пароль"})
    submit = SubmitField('Войти')
