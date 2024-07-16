from flaskblog import create_app


# Create the Flask application instance using create_app function
app = create_app()


# Run the Flask application if this script is executed directly
if __name__ == '__main__':
	app.run(debug=True)
