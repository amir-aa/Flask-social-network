from flask_wtf import Form
from models import  User
from peewee import *
from wtforms import StringField,PasswordField,RadioField,TextAreaField
from flask_wtf.file import FileField, FileAllowed,FileRequired

from wtforms.validators import regexp,DataRequired,email,Length,EqualTo

#-------------------------------------------------------------
#Check if email or Username Exists
def duplicatesuser(form,field):
    if(User.select().where(User.username==field.data).exists()):
        raise ValueError('already exists')
def duplicateemail(form,field):
    if (User.select().where(User.Email == field.data).exists()):
        raise ValueError('already exists')
#---------------------------------------------------------------
class regform(Form):
    username = StringField('username', validators=[DataRequired(),regexp(r'^[a-zA-Z0-9_]+$',message='Letter & Number only'),duplicatesuser])
    email = StringField('email',validators=[DataRequired('it is neccessary'),email(),duplicateemail])
    gender = RadioField('gender',choices = [('M','Male'),('F','Female')])
    image=FileField('image')
    #enctype="multipart/form-data" is necessary on HTML Page
    password = PasswordField('Password',validators=[DataRequired(),Length(min=3),EqualTo('password2',message='password should match')])
    password2=PasswordField('Confirm Password',validators=[DataRequired()])

class Loginform(Form):
    username=StringField('username', validators=[DataRequired(),regexp(r'^[a-zA-Z0-9_]+$',message='Letter & Number only')])
    password=PasswordField('password',validators=[DataRequired()])
class post_form(Form):
    content=TextAreaField("Whats UP ?!!",validators=[DataRequired()])