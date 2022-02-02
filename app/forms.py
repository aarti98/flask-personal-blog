from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
    
class CommentForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    comment = TextAreaField('Comment', validators = [DataRequired()])
    submit = SubmitField('Post')


class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    login = SubmitField('Login')


class BlogForm(FlaskForm):
    title = StringField('Name', validators = [DataRequired()])
    content = TextAreaField('Content', validators = [DataRequired()])
    submit = SubmitField('Post')


class BlogUpdateForm(FlaskForm):
    title = StringField('Name', validators = [DataRequired()])
    content = TextAreaField('Content', validators = [DataRequired()])
    update = SubmitField('Update Blog')


class BlogDeleteForm(FlaskForm):
    delete = SubmitField('Delete Blog')