from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, DataRequired
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登陆')

class RegistrationForm(FlaskForm):
	email = StringField('邮箱', validators=[Required(), Length(1, 64),Email()])
	username = StringField('用户名', validators=[
							Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
							'Usernames must have only letters, '
							'numbers, dots or underscores')])
	password = PasswordField('密码', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('确认密码', validators=[Required()])
	submit = SubmitField('注册')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱已存在')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('用户名已存在')

class ChangePasswordForm(FlaskForm):
	password_old = PasswordField('旧密码', validators=[Required()])
	password = PasswordField('新密码', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('确认密码', validators=[Required()])
	submit = SubmitField('更新')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('重置密码')

class PasswordResetForm(FlaskForm):
	password = PasswordField('新密码', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('确认密码', validators=[Required()])
	submit = SubmitField('确认重置密码')

class ChangeEmailForm(FlaskForm):
	email = StringField('新邮箱', validators=[DataRequired(), Length(1, 64), Email()])
	password = PasswordField('密码', validators=[Required()])
	submit = SubmitField('更新邮箱地址')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱已存在')