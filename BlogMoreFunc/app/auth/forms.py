from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, DataRequired
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
	email = StringField('Email', validators=[Required(), Length(1, 64),Email()])
	username = StringField('Username', validators=[
							Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
							'Usernames must have only letters, '
							'numbers, dots or underscores')])
	password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Register')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')

class ChangePasswordForm(FlaskForm):
	password_old = PasswordField('Old password', validators=[Required()])
	password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Update')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Reset Password')

class PasswordResetForm(FlaskForm):
	password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Confirm Reset Password')

class ChangeEmailForm(FlaskForm):
	email = StringField('New Email', validators=[DataRequired(), Length(1, 64), Email()])
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Update Email Address')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.') 