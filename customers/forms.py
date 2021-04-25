from wtforms import Form, StringField, PasswordField, SubmitField, validators, ValidationError
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from .model import Register


class CustomerRegisterForm(FlaskForm):
    name = StringField('Имя: ')
    username = StringField('Имя пользователя: ', [validators.DataRequired()])
    email = EmailField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Пароль: ', [validators.DataRequired(), validators.EqualTo('confirm', message='Оба пароля должны совпадать')])
    confirm = PasswordField('Повтор пароля: ', [validators.DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("Имя пользователя недоступно!")
        
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("Этот email уже зарегистрирован!")


class CustomerLoginFrom(FlaskForm):
    email = EmailField('Почта', [validators.DataRequired()])
    password = PasswordField('Пароль: ', [validators.DataRequired()])

   




   

 

    

     

   


    

