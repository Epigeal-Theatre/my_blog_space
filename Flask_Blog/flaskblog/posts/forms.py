from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
	"""
    Form class for creating or updating a post.

    Attributes:
    -----------
    title : StringField
        Field for entering the title of the post.
        Validators:
            - DataRequired: Ensures the field is not submitted empty.

    content : TextAreaField
        Field for entering the content of the post.
        Validators:
            - DataRequired: Ensures the field is not submitted empty.

    submit : SubmitField
        Button for submitting the post form.
    """
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Post')
