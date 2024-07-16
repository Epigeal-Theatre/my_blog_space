from datetime import datetime# Importing datetime module for date and time operations
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer# Importing Serializer from itsdangerous module for token serialization
from flask import current_app# Importing current_app from Flask for accessing current application context
from flaskblog import db, login_manager# Importing db and login_manager from flaskblog package
from flask_login import UserMixin# Importing UserMixin from Flask-Login for user session management

@login_manager.user_loader
def load_user(user_id):# Function to load a user from the database based on user_id
	return User.query.get(int(user_id))# Returns the User object corresponding to user_id



# Defining the User class which inherits from db.Model for database functionality
# and UserMixin for Flask-Login integration
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username =  db.Column(db.String(20), unique=True,nullable=False)
	email = db.Column(db.String(120), unique=True,nullable=False)
	image_file = db.Column(db.String(20),nullable=False, default = 'default.jpg')
	password = db.Column(db.String(60),nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)
	#by Setting up a relationship with the 'posts' table using db.relationship,
    # allowing access to Post objects associated with a User through 'author'




	def get_reset_token(self, expires_sec=1800):

		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		"""
        Generate a reset token for the user that expires in a specified number of seconds.

        Parameters:
        expires_sec (int): Number of seconds before the token expires.
        Defaults to 1800 seconds (30 minutes).

        Returns:
        str: The generated reset token as a UTF-8 encoded string.
        """
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)



	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.image_file}')"


class Post(db.Model):
	"""
    Post model represents a blog post in the database.

    Attributes:
        id (int): The unique identifier for each post, primary key.
        title (str): The title of the post, maximum length of 100 characters.
        date_posted (datetime): The date and time when the post was created.
        content (str): The content of the post.
        user_id (int): The ID of the user who created the post, foreign key.
    """
	id = db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id =db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		"""
        Return a string representation of the Post instance.

        Returns:
            str: String representation of the post.
        """
		return f"Post('{self.title}','{self.date_posted}',)"