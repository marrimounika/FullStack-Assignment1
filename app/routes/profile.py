import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Profile, User
from app.forms import ProfileForm, ChangePasswordForm
from werkzeug.utils import secure_filename
from PIL import Image

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@profile_bp.route('/', methods=['GET'])
@login_required
def view_profile():
    """View the current user's profile."""
    profile = current_user.profile
    return render_template('profile/view_profile.html', profile=profile)


@profile_bp.route('/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    """Update the current user's profile or change password."""
    profile = current_user.profile
    form_profile = ProfileForm(obj=profile)
    form_password = ChangePasswordForm()

    if request.method == 'POST':
        # Handle profile updates
        if 'submit_profile' in request.form and form_profile.validate_on_submit():
            # Check if the new username is different and unique
            if form_profile.username.data != current_user.username:
                existing_user = User.query.filter_by(username=form_profile.username.data).first()
                if existing_user:
                    flash('Username already taken. Please choose a different one.', 'danger')
                    return redirect(url_for('profile.update_profile'))
                current_user.username = form_profile.username.data

            # Update or create profile fields
            if profile:
                form_profile.populate_obj(profile)
            else:
                profile = Profile(
                    reading_preferences=form_profile.reading_preferences.data,
                    favorite_genres=form_profile.favorite_genres.data,
                    books_wanted=form_profile.books_wanted.data,
                    user_id=current_user.id
                )
                db.session.add(profile)

            # Handle avatar upload
            if form_profile.avatar.data:
                file = form_profile.avatar.data
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = int(datetime.utcnow().timestamp())
                    filename = f"user_{current_user.id}_{timestamp}{os.path.splitext(filename)[1]}"

                    # Define the upload path
                    upload_path = os.path.join(current_app.root_path, 'static/uploads/profile')
                    os.makedirs(upload_path, exist_ok=True)

                    file_path = os.path.join(upload_path, filename)
                    file.save(file_path)

                    # Resize image
                    try:
                        img = Image.open(file_path)
                        img.thumbnail((300, 300))
                        img.save(file_path)
                    except Exception as e:
                        flash(f"Failed to process avatar image: {e}", 'danger')
                        os.remove(file_path)
                        return redirect(url_for('profile.update_profile'))

                    # Delete old avatar
                    if profile.avatar and profile.avatar != 'default_avatar.png':
                        old_avatar_path = os.path.join(upload_path, profile.avatar)
                        if os.path.exists(old_avatar_path):
                            os.remove(old_avatar_path)

                    profile.avatar = filename

            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile.view_profile'))

        # Handle password updates
        if 'submit_password' in request.form and form_password.validate_on_submit():
            if not current_user.check_password(form_password.current_password.data):
                flash('Current password is incorrect.', 'danger')
            elif form_password.new_password.data != form_password.confirm_new_password.data:
                flash('New passwords do not match.', 'danger')
            else:
                current_user.set_password(form_password.new_password.data)
                db.session.commit()
                flash('Password updated successfully!', 'success')
                return redirect(url_for('profile.view_profile'))

    return render_template(
        'profile/update_profile.html',
        form_profile=form_profile,
        form_password=form_password
    )
