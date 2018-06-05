from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, DataRequired
from wtforms import ValidationError
from ..models import User, Role
from flask_pagedown.fields import PageDownField


class EditProfileForm(FlaskForm):
	name = StringField('真实姓名', validators=[Length(0, 64)])
	location = StringField('所在地', validators=[Length(0, 64)])
	about_me = TextAreaField('个人简介')
	submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
	email = StringField('邮箱', validators=[Required(), Length(1, 64),	Email()])
	username = StringField('用户名',
							validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, \
							'Usernames must have only letters, numbers, dots or underscores')])
	confirmed = BooleanField('确认')
	role = SelectField('用户角色', coerce=int)
	name = StringField('真实姓名', validators=[Length(0, 64)])
	location = StringField('所在地', validators=[Length(0, 64)])
	about_me = TextAreaField('个人简介')
	submit = SubmitField('提交')

	def __init__(self, user, *args, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
		self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def validate_email(self, field):
		if field.data != self.user.email and User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱已存在')

	def validate_username(self, field):
		if field.data != self.user.username and User.query.filter_by(username=field.data).first():
			raise ValidationError('用户名已存在')


class PostForm(FlaskForm):
	title = StringField('请输入文章标题', validators=[Length(0, 64)])
	body = PageDownField("博客正文", validators=[Required()])
	submit = SubmitField('发布博客')


class CommentForm(FlaskForm):
    body = StringField('相对作者说点什么', validators=[DataRequired()])
    submit = SubmitField('发表评论')