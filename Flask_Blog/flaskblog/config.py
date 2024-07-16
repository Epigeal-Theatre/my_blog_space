import os

# Setting up class variables for configuration
class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')# Fetching the SECRET_KEY from environment variables
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')# Fetching the SQLALCHEMY_DATABASE_URI from environment variables
	MAIL_SERVER = 'smtp.gmail.com'# Gmail SMTP server address
	MAIL_PORT = 587# Port for TLS connection
	MAIL_USE_TLS = True# Using TLS encryption for email transport
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
