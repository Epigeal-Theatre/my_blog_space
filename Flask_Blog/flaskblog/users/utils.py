import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_picture(form_picture):
	"""
    Function to save a profile picture uploaded via a form.

    Parameters:
    -----------
    form_picture : FileStorage
        The picture file uploaded via the form.

    Returns:
    --------
    picture_fn : str
        The filename of the saved picture.
    """
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path,'static/assets', picture_fn)

	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn


def send_reset_email(user):
	"""
    Function to send a password reset email to the user.

    Parameters:
    -----------
    user : User
        The user object for whom the password reset email is being sent.

    Sends an email with a password reset link to the user's registered email address.
    """
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='dantestdevs@gmail.com', recipients=[user.email])
	msg.body =  f'''To Reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, ignore this email and no changes will be made'''

	try:
		mail.send(msg)
	except Exception as e:
		print(f"Failed to send email: {e}")