from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import ExchangeRequest, Book, User
from app.forms import ExchangeRequestForm, RespondExchangeForm

exchanges_bp = Blueprint('exchanges', __name__, url_prefix='/exchanges')

@exchanges_bp.route('/request/<int:book_id>', methods=['GET', 'POST'])
@login_required
def request_exchange(book_id):
    book = Book.query.get_or_404(book_id)
    
    # Prevent users from requesting their own books
    if book.user_id == current_user.id:
        flash('You cannot exchange your own book.', 'warning')
        return redirect(url_for('books.search_books'))
    
    form = ExchangeRequestForm()
    if form.validate_on_submit():
        exchange_request = ExchangeRequest(
            sender_id=current_user.id,
            receiver_id=book.user_id,  # Ensure the receiver is the book's owner
            book_id=book.id,
            delivery_method=form.delivery_method.data,
            exchange_duration=form.exchange_duration.data,
            status='pending'
        )
        db.session.add(exchange_request)
        db.session.commit()
        flash('Exchange request sent!', 'success')
        # Optional: Notify the receiver about the exchange request
        return redirect(url_for('exchanges.view_requests'))
    
    return render_template('exchanges/request_exchange.html', form=form, book=book)

@exchanges_bp.route('/view', methods=['GET'])
@login_required
def view_requests():
    # Fetch requests received by the user
    received_requests = ExchangeRequest.query.filter_by(receiver_id=current_user.id).order_by(ExchangeRequest.timestamp.desc()).all()
    # Fetch requests sent by the user
    sent_requests = ExchangeRequest.query.filter_by(sender_id=current_user.id).order_by(ExchangeRequest.timestamp.desc()).all()
    
    # Initialize response forms for each received request
    respond_forms = {req.id: RespondExchangeForm() for req in received_requests}
    
    return render_template('exchanges/view_requests.html', received_requests=received_requests, sent_requests=sent_requests, respond_forms=respond_forms)

@exchanges_bp.route('/respond/<int:request_id>', methods=['POST'])
@login_required
def respond_exchange(request_id):
    # Fetch the exchange request
    exchange_request = ExchangeRequest.query.get_or_404(request_id)
    
    # Ensure the current user is the intended recipient of the request
    if exchange_request.receiver_id != current_user.id:
        flash('You are not authorized to respond to this request.', 'danger')
        return redirect(url_for('exchanges.view_requests'))

    # Handle form submission
    form = RespondExchangeForm()
    if form.validate_on_submit():
        # Check which button was clicked
        if 'submit_accept' in request.form:
            if exchange_request.status == 'pending':  # Ensure request is still pending
                exchange_request.status = 'accepted'
                # Optional: Mark the book as unavailable
                book = exchange_request.book
                book.availability_status = 'unavailable'
                db.session.commit()
                flash('Exchange request accepted.', 'success')
            else:
                flash('This exchange request has already been processed.', 'warning')
        elif 'submit_reject' in request.form:
            if exchange_request.status == 'pending':  # Ensure request is still pending
                exchange_request.status = 'rejected'
                db.session.commit()
                flash('Exchange request rejected.', 'info')
            else:
                flash('This exchange request has already been processed.', 'warning')
        else:
            flash('Invalid action.', 'danger')
    else:
        flash('Invalid form submission.', 'danger')

    return redirect(url_for('exchanges.view_requests'))
