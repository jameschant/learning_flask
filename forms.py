from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(Form):
    first_name = StringField('First name', validators=[DataRequired("First name required.")])
    last_name = StringField('Last name', validators=[DataRequired("Last name required.")])
    email = StringField('Email', validators=[DataRequired("Email required."), Email("Please enter a valid email address.")])
    password = PasswordField('Password', validators=[DataRequired("Password required."), Length(min=6, message="Password must be more than 6 characters long.")])
    submit = SubmitField('Sign up')


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
    submit = SubmitField("Sign in")


class AddressForm(Form):
    address = StringField('Address', validators=[DataRequired("Please enter an address.")])
    submit = SubmitField('Search')