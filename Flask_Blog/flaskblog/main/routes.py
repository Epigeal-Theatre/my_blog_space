from flask import render_template, request, Blueprint
from flaskblog.models import Post


main =Blueprint('main', __name__)
"""
Blueprint for main routes in the Flask application.

This blueprint is used to organize routes related to the main functionality
of the application, such as the home page, about page, etc.

Attributes:
-----------
'main' : Blueprint
    The Blueprint instance for main routes.

__name__ : str
    The name of the current Python module.

Returns:
--------
Blueprint
    The 'main' Blueprint instance for registering with the Flask application.
"""



@main.route("/")
@main.route("/home")
def home():
	"""
    Route for displaying the home page.

    GET:
    - Retrieves posts from the database, ordered by date posted in descending order.
    - Paginates the posts to display a limited number per page.
    - Renders the home.html template with paginated posts.

    Returns:
    --------
    Renders the home.html template with paginated posts.
    """
	page = request.args.get('page',1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('home.html', posts=posts)


@main.route("/about")
def about():
	"""
    Route for displaying the about page.

    GET:
    - Renders the about.html template with title 'About'.

    Returns:
    --------
    Renders the about.html template with title 'About'.
    """
	return render_template('about.html', title='About')