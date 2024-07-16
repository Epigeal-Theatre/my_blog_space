from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts =Blueprint('posts', __name__)
"""
Blueprint for post-related routes in the Flask application.

This blueprint is used to organize routes related to posts, such as creating,
viewing, updating, and deleting posts.

Attributes:
-----------
'posts' : Blueprint
    The Blueprint instance for post-related routes.

__name__ : str
    The name of the current Python module.

Returns:
--------
Blueprint
    The 'posts' Blueprint instance for registering with the Flask application.
"""


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	"""
    Route for creating a new post.

    GET:
    - Renders the create_post.html template with a PostForm instance for creating a new post.

    POST:
    - Processes the PostForm data upon form submission.
    - Creates a new Post object in the database with the submitted title, content, and current user as the author.
    - Redirects to the home page upon successful post creation and displays a success message.

    Returns:
    --------
    GET: Renders the create_post.html template with the PostForm instance.
    POST: Redirects to the home page after creating the new post.
    """
	form = PostForm()
	if form.validate_on_submit():
		post=Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your Post has been Created Successfully.', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_post.html', title= 'New Post', form=form, legend='New Post')




@posts.route("/post/<int:post_id>")
def post(post_id):
	"""
    Route for displaying a specific post.

    Parameters:
    -----------
    post_id : int
        The unique identifier of the post to be displayed.

    Returns:
    --------
    Renders the post.html template with the specified post's title and content.
    """
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	"""
    Route for updating an existing post.

    Parameters:
    -----------
    post_id : int
        The unique identifier of the post to be updated.

    GET:
    - Retrieves the existing post from the database.
    - Populates the PostForm with the current post data for editing.

    POST:
    - Processes the PostForm data upon form submission.
    - Updates the post's title and content in the database.
    - Redirects to the updated post's page upon successful update and displays a success message.
    - Aborts with a 403 error if the current user is not the author of the post.

    Returns:
    --------
    GET: Renders the create_post.html template with the 
    PostForm instance populated with current post data.

    POST: Redirects to the updated post's page after successfully updating the post.
    """
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title= form.title.data
		post.content= form.content.data
		db.session.commit()
		flash('You have successfully updated your post', 'success')
		return redirect(url_for('posts.post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')



@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	"""
    Route for deleting an existing post.

    Parameters:
    -----------
    post_id : int
        The unique identifier of the post to be deleted.

    POST:
    - Retrieves the existing post from the database.
    - Checks if the current user is the author of the post.
    - Deletes the post from the database upon authorization.
    - Redirects to the home page after successful deletion and displays a success message.
    - Aborts with a 403 error if the current user is not the author of the post.

    Returns:
    --------
    Redirects to the home page after successfully deleting the post.
    """
	post = Post.query.get_or_404(post_id)
	# Check if the current user is the author of the post
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('You have successfully deleted your post!', 'success')
	return redirect(url_for('main.home'))
