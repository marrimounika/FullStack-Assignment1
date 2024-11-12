import os
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Book
from app.forms import BookForm, SearchForm
from werkzeug.utils import secure_filename
from sqlalchemy import or_
from PIL import Image

books_bp = Blueprint('books', __name__, url_prefix='/books')


def allowed_file(filename):
    """Check if the file has an allowed extension."""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@books_bp.route('/', methods=['GET'])
@login_required
def list_books():
    """List all books owned by the current user."""
    page = request.args.get('page', 1, type=int)
    per_page = 9  # Number of books per page
    books_pagination = Book.query.filter_by(user_id=current_user.id).order_by(Book.date_posted.desc()).paginate(page=page, per_page=per_page, error_out=False)
    books = books_pagination.items
    return render_template('books/list_books.html', books=books, pagination=books_pagination)


@books_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_book():
    """Add a new book."""
    form = BookForm()
    if form.validate_on_submit():
        filename = None
        if form.cover_image.data:
            file = form.cover_image.data
            if allowed_file(file.filename):
                try:
                    # Secure the filename and add a timestamp for uniqueness
                    raw_filename = secure_filename(file.filename)
                    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
                    filename = f"book_{current_user.id}_{timestamp}{os.path.splitext(raw_filename)[1]}"

                    # Define the upload directory
                    uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'books')
                    os.makedirs(uploads_dir, exist_ok=True)

                    # Save the file
                    file_path = os.path.join(uploads_dir, filename)
                    file.save(file_path)
                    print(f"File saved to: {file_path}")

                    # Resize the image
                    img = Image.open(file_path)
                    img.thumbnail((300, 300))  # Resize to max 300x300 pixels
                    img.save(file_path)
                    print(f"Image resized and saved: {file_path}")
                except Exception as e:
                    flash(f"Failed to upload or process the image: {e}", 'danger')
                    return redirect(request.url)
            else:
                flash('File type not allowed.', 'danger')
                return redirect(request.url)

        # Add the book to the database
        book = Book(
            title=form.title.data,
            author=form.author.data,
            genre=form.genre.data,
            condition=form.condition.data,
            availability_status=form.availability_status.data,
            location=form.location.data,
            cover_image=filename,
            user_id=current_user.id
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('books.list_books'))
    return render_template('books/add_book.html', form=form)


@books_bp.route('/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    """Edit an existing book."""
    book = Book.query.get_or_404(book_id)
    if book.user_id != current_user.id:
        flash('You are not authorized to edit this book.', 'danger')
        return redirect(url_for('books.list_books'))
    form = BookForm(obj=book)
    if form.validate_on_submit():
        # Handle file upload
        if form.cover_image.data:
            file = form.cover_image.data
            if allowed_file(file.filename):
                try:
                    # Secure the filename
                    raw_filename = secure_filename(file.filename)
                    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
                    filename = f"book_{current_user.id}_{timestamp}{os.path.splitext(raw_filename)[1]}"

                    # Define the upload directory
                    uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'books')
                    os.makedirs(uploads_dir, exist_ok=True)

                    # Save the new file
                    file_path = os.path.join(uploads_dir, filename)
                    file.save(file_path)

                    # Resize the image
                    img = Image.open(file_path)
                    img.thumbnail((300, 300))
                    img.save(file_path)

                    # Delete the old file if it exists
                    if book.cover_image:
                        old_file_path = os.path.join(uploads_dir, book.cover_image)
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)

                    # Update the book's cover image
                    book.cover_image = filename
                except Exception as e:
                    flash(f"Failed to upload or process the image: {e}", "danger")
                    if filename and os.path.exists(file_path):
                        os.remove(file_path)
                    return redirect(request.url)
            else:
                flash('File type not allowed.', 'danger')
                return redirect(request.url)

        # Update other book fields
        book.title = form.title.data
        book.author = form.author.data
        book.genre = form.genre.data
        book.condition = form.condition.data
        book.availability_status = form.availability_status.data
        book.location = form.location.data
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('books.list_books'))
    return render_template('books/edit_book.html', form=form, book=book)


@books_bp.route('/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    """Delete a book."""
    book = Book.query.get_or_404(book_id)
    if book.user_id != current_user.id:
        flash('You are not authorized to delete this book.', 'danger')
        return redirect(url_for('books.list_books'))

    # Delete cover image file if it exists
    if book.cover_image:
        uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'books')
        file_path = os.path.join(uploads_dir, book.cover_image)
        if os.path.exists(file_path):
            os.remove(file_path)

    # Delete the book record
    db.session.delete(book)
    db.session.commit()
    flash('Book has been deleted!', 'success')
    return redirect(url_for('books.list_books'))


@books_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search_books():
    """Search books based on various filters."""
    form = SearchForm()
    books = []
    if form.validate_on_submit():
        query = Book.query
        if form.search_query.data:
            search = f"%{form.search_query.data}%"
            query = query.filter(or_(Book.title.ilike(search), Book.author.ilike(search), Book.genre.ilike(search)))
        if form.genre.data:
            query = query.filter(Book.genre.ilike(f"%{form.genre.data}%"))
        if form.availability_status.data:
            query = query.filter_by(availability_status=form.availability_status.data)
        if form.location.data:
            query = query.filter(Book.location.ilike(f"%{form.location.data}%"))
        books = query.paginate(page=request.args.get('page', 1, type=int), per_page=10)
    return render_template('books/search_books.html', form=form, books=books)
