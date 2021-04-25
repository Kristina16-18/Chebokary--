from wtforms import TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import Form
from wtforms import StringField
from wtforms import validators


class Book_obj(Form):
    name = StringField('Имя', [validators.DataRequired()])
    author = StringField('Автор', [validators.DataRequired()])
    discription = TextAreaField('Описание', [validators.DataRequired()])

    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])

    def __repr__(self):
        return '<Post %r>' % self.name
