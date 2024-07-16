from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
	"""
	A form for user registration.

	Attributes:
	-----------
	username : StringField
		Field for the username input, requires data and length validation.
	email : StringField
		Field for the email input, requires data and email format validation.
	password : PasswordField
		Field for the password input, requires data validation.
	confirm_password : PasswordField
		Field to confirm the password input, requires data and equality validation.
	submit : SubmitField
		Field for the form submission button.
	"""
	username = StringField('Username', validators=[DataRequired(), Length(min= 2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		"""
		Custom validator for the username field.

		Checks if the username already exists in the database.

		Parameters:
		-----------
		username : StringField
			The field representing the username to be validated.

		Raises:
		-------
		ValidationError
			If the username already exists in the database.
		"""
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is not available. Try another one')

	def validate_email(self, email):
		"""
		Custom validator for the email field.

		Checks if the email already exists in the database.

		Parameters:
		-----------
		email : StringField
			The field representing the email to be validated.

		Raises:
		-------
		ValidationError
			If the email already exists in the database.
		"""
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email has been taken. Try another one')


class LoginForm(FlaskForm):
	"""
	A form for user login.

	Attributes:
	-----------
	email : StringField
		Field for the email input, requires data and email format validation.
	password : PasswordField
		Field for the password input, requires data validation.
	remember : BooleanField
		Field to remember the user's login session.
	submit : SubmitField
		Field for the form submission button.
	"""
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), ])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	"""
	A form for updating user account information.

	Attributes:
	-----------
	username : StringField
		Field for the username input, requires data and length validation.
	email : StringField
		Field for the email input, requires data and email format validation.
	picture : FileField
		Field for updating the user's profile picture, allows only 'jpg' and 'png' file types.
	submit : SubmitField
		Field for the form submission button.
	"""
	username = StringField('Username', validators=[DataRequired(), Length(min= 2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	
	submit = SubmitField('Update')

	def validate_username(self, username):
		"""
		Custom validator for the username field during account update.

		Checks if the new username already exists in the database and is different from the current user's username.

		Parameters:
		-----------
		username : StringField
			The field representing the new username to be validated.

		Raises:
		-------
		ValidationError
			If the username already exists in the database and is different from the current user's username.
		"""
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username is not available. Try another one')

	def validate_email(self, email):
		"""
		Custom validator for the email field during account update.

		Checks if the new email already exists in the database and is different from the current user's email.

		Parameters:
		-----------
		email : StringField
			The field representing the new email to be validated.

		Raises:
		-------
		ValidationError
			If the email already exists in the database and is different from the current user's email.
		"""
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email has been taken. Try another one')


class RequestResetForm(FlaskForm):
	"""
	A form for requesting a password reset.

	Attributes:
	-----------
	email : StringField
		Field for the email input, requires data and email format validation.
	submit : SubmitField
		Field for the form submission button.
	"""
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		"""
		Custom validator for the email field during password reset request.

		Checks if the email exists in the database.

		Parameters:
		-----------
		email : StringField
			The field representing the email to be validated.

		Raises:
		-------
		ValidationError
			If no account with the provided email exists in the database.
		"""
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('An account with that email does not exist. You must Register first')


class ResetPasswordForm(FlaskForm):
	"""
	A form for resetting the password.

	Attributes:
	-----------
	password : PasswordField
		Field for the new password input, requires data validation.
	confirm_password : PasswordField
		Field to confirm the new password input, requires data and equality validation.
	submit : SubmitField
		Field for the form submission button.
	"""
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')
