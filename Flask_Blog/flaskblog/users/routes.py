from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email


users =Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
	"""
    Route for user registration.

    If the user is already authenticated, redirects to the home page.
    Processes the RegistrationForm data, hashes the password, creates a new user, and commits to the database.

    Returns:
    --------
    GET: Renders the register.html template with the RegistrationForm instance.
    POST: If form validation succeeds, redirects to the login page after creating the user account.
          If form validation fails, re-renders the register.html template with the form instance containing errors.
    """
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your Account has Been created! You can now log in!', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title= 'Register', form=form)



@users.route('/login', methods=['GET', 'POST'])
def login():
	"""
    Route for user login.

    If the user is already authenticated, redirects to the home page.
    Processes the LoginForm data, verifies the credentials, and logs in the user if valid.

    Returns:
    --------
    GET: Renders the login.html template with the LoginForm instance.
    POST: If form validation succeeds and credentials are correct, logs in the user and redirects to the next page or home.
          If form validation fails, re-renders the login.html template with the form instance containing errors.
    """
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user= User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Login not successful.Check your Email and Password', 'danger')
	return render_template('login.html', title= 'Login', form=form)



@users.route('/logout')
def logout():
	"""
    Route for user logout.

    Logs out the current user and redirects to the home page.

    Returns:
    --------
    Redirects to the home page.
    """
	logout_user()
	return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	"""
	Route for user account management.

	GET:
	- Renders the account.html template with the UpdateAccountForm instance.
	- Pre-populates the form fields with the current user's username and email.

	POST:
	- Processes the UpdateAccountForm data.
	- Updates the current user's username, email, and profile picture (if provided).
	- Commits the changes to the database and redirects to the account page.
	- Displays a success message upon successful update.

	Returns:
	--------
	GET: Renders the account.html template with the current user's profile picture and UpdateAccountForm instance.
	POST: Redirects to the account page after processing the form data and updating the user's account details.
	"""
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('You have successfully updated your account', 'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='assets/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form)




@users.route("/user/<string:username>")
def user_posts(username):
	"""
    Route for displaying posts by a specific user.

    Parameters:
    -----------
    username : str
        The username of the user whose posts are to be displayed.

    Returns:
    --------
    Renders the user_post.html template with paginated posts and user information.
    """
	page = request.args.get('page',1, type=int)
	user =User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('user_post.html', posts=posts, user=user)




@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
	"""
    Route for initiating a password reset request.

    GET:
    - Renders the reset_request.html template with the RequestResetForm instance.
    - Redirects to the home page if the user is already authenticated.

    POST:
    - Processes the RequestResetForm data.
    - Sends a reset password email to the user's registered email address.
    - Displays a notification message upon successful submission.

    Returns:
    --------
    GET: Renders the reset_request.html template with the RequestResetForm instance.
    POST: Redirects to the login page after sending the reset password email.
    """
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email with instructions on resetting your password has been sent', 'info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html', title='Reset Password', form=form)





@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
	"""
    Route for resetting the password using a token.

    Parameters:
    -----------
    token : str
        The token received in the password reset request email.

    GET:
    - Verifies the token and renders the reset_token.html template with the ResetPasswordForm instance.
    - Redirects to the home page if the user is already authenticated.
    - Displays a warning message if the token is expired or invalid, and redirects to the reset_request route.

    POST:
    - Processes the ResetPasswordForm data.
    - Updates the user's password in the database after successful form validation.
    - Displays a success message upon password update and redirects to the login page.

    Returns:
    --------
    GET: Renders the reset_token.html template with the ResetPasswordForm instance.
    POST: Redirects to the login page after updating the user's password.
    """
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('The token is either expired or invalid', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Your password has been Updated! You can now proceed to log in', 'success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title= 'Reset Password', form=form)
