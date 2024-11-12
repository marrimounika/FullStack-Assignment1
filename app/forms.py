# app/forms.py

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    SelectField,
    TextAreaField,
    FileField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    ValidationError,
    Length
)
from flask_wtf.file import FileAllowed
from app.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        # Check if the user is authenticated before comparing their username
        if current_user.is_authenticated and username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    submit = SubmitField('Reset Password')

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    author = StringField('Author', validators=[DataRequired(), Length(max=100)])
    genre = StringField('Genre', validators=[DataRequired(), Length(max=50)])
    condition = SelectField('Condition', choices=[
        ('New', 'New'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Poor', 'Poor')
    ], validators=[DataRequired()])
    availability_status = SelectField('Availability', choices=[
        ('available', 'Available'),
        ('unavailable', 'Unavailable')
    ], validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), Length(max=100)])
    cover_image = FileField('Book Cover Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf'], 'Images and PDFs only!')
    ])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    search_query = StringField('Search', validators=[DataRequired(), Length(max=100)])
    genre = StringField('Genre', validators=[Length(max=50)])
    availability_status = SelectField('Availability', choices=[
        ('', 'Any'),
        ('available', 'Available'),
        ('unavailable', 'Unavailable')
    ])
    location = StringField('Location', validators=[Length(max=100)])
    submit = SubmitField('Search')

class ExchangeRequestFormv(FlaskForm):
    delivery_method = StringField('Delivery Method', validators=[
        DataRequired(message="Delivery method is required."),
        Length(max=50, message="Delivery method must be under 50 characters.")
    ])
    exchange_duration = StringField('Exchange Duration', validators=[
        DataRequired(message="Exchange duration is required."),
        Length(max=50, message="Exchange duration must be under 50 characters.")
    ])
    submit = SubmitField('Request Exchange')

class ExchangeRequestForm(FlaskForm):
    delivery_method = StringField('Delivery Method', validators=[DataRequired(), Length(max=50)])
    exchange_duration = StringField('Exchange Duration', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Send Request')

class RespondExchangeForm(FlaskForm):
    submit_accept = SubmitField('Accept')
    submit_reject = SubmitField('Reject')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    reading_preferences = TextAreaField('Reading Preferences', validators=[
        Length(max=500, message="Reading preferences must be under 500 characters.")
    ])
    favorite_genres = StringField('Favorite Genres', validators=[
        Length(max=100, message="Favorite genres must be under 100 characters.")
    ])
    books_wanted = TextAreaField('Books Wanted', validators=[
        Length(max=500, message="Books wanted must be under 500 characters.")
    ])
    avatar = FileField('Update Profile Picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    submit_profile = SubmitField('Update Profile')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[
        DataRequired()
    ])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=6, message="Password must be at least 6 characters long.")
    ])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message="Passwords must match.")
    ])
    submit_password = SubmitField('Change Password')

class MessageForm(FlaskForm):
    content = TextAreaField('Message', validators=[
        DataRequired(),
        Length(min=1, max=1000, message="Message must be between 1 and 1000 characters.")
    ])
    submit = SubmitField('Send')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[
        DataRequired(message="Please enter your current password.")
    ])
    new_password = PasswordField('New Password', validators=[
        DataRequired(message="Please enter a new password."),
        Length(min=6, message="Password must be at least 6 characters long.")
    ])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message="Please confirm your new password."),
        EqualTo('new_password', message="Passwords must match.")
    ])
    submit_password = SubmitField('Update Password')