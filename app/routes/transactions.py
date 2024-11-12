# app/routes/transactions.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import ExchangeRequest, Transaction

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@transactions_bp.route('/')
@login_required
def manage_transactions():
    # Fetch all exchange requests related to the user
    sent_requests = ExchangeRequest.query.filter_by(sender_id=current_user.id).order_by(ExchangeRequest.timestamp.desc()).all()
    received_requests = ExchangeRequest.query.filter_by(receiver_id=current_user.id).order_by(ExchangeRequest.timestamp.desc()).all()
    return render_template('transactions/manage_transactions.html', sent_requests=sent_requests, received_requests=received_requests)

@transactions_bp.route('/cancel/<int:request_id>', methods=['POST'])
@login_required
def cancel_transaction(request_id):
    exchange_request = ExchangeRequest.query.get_or_404(request_id)
    if exchange_request.sender != current_user and exchange_request.receiver != current_user:
        flash('You are not authorized to cancel this transaction.', 'danger')
        return redirect(url_for('transactions.manage_transactions'))
    if exchange_request.status not in ['pending', 'accepted']:
        flash('Cannot cancel this transaction.', 'warning')
        return redirect(url_for('transactions.manage_transactions'))
    exchange_request.status = 'canceled'
    db.session.commit()
    flash('Transaction canceled.', 'info')
    return redirect(url_for('transactions.manage_transactions'))
