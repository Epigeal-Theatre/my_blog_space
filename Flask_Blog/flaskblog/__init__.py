from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager= LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()



def create_app(config_class=Config):
	"""
    Factory function to create and configure the Flask application.

    Parameters:
    -----------
    config_class : class
        The configuration class to use for the application settings.

    Returns:
    --------
    app : Flask
        The configured Flask application instance.
    """
	app = Flask(__name__)
	app.config.from_object(Config)

	

	# Initialize extensions with the app instance
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)



	# Import and register blueprints
	from flaskblog.users.routes import users
	from flaskblog.posts.routes import posts
	from flaskblog.main.routes import main
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)


	return app