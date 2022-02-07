from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from flask_ckeditor import CKEditorField 
from app.models import User
    
class CommentForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    comment = TextAreaField('Comment', validators = [DataRequired()])
    
    submit = SubmitField('Post')

class BlogForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    description = StringField('Description', validators = [DataRequired()])
    content = CKEditorField('Content', validators = [DataRequired()])
    
    submit = SubmitField('Post')


class BlogUpdateForm(FlaskForm):
    title = StringField('Name', validators = [DataRequired()])
    description = StringField('Description', validators = [DataRequired()])
    content = CKEditorField('Content', validators = [DataRequired()])
    
    update = SubmitField('Update Blog')


class BlogDeleteForm(FlaskForm):
    delete = SubmitField('Delete Blog')


class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    
    login = SubmitField('Login')


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')
