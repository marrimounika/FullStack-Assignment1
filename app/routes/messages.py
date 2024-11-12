from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Message, User
from app.forms import MessageForm  # Ensure you have a MessageForm defined

messages_bp = Blueprint('messages', __name__, url_prefix='/messages')

@messages_bp.route('/send/<int:receiver_id>', methods=['GET', 'POST'])
@login_required
def send_message(receiver_id):
    receiver = User.query.get_or_404(receiver_id)
    if receiver == current_user:
        flash('You cannot send messages to yourself.', 'warning')
        return redirect(url_for('messages.inbox'))
    
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(
            sender_id=current_user.id,
            receiver_id=receiver.id,
            content=form.content.data
        )
        db.session.add(message)
        db.session.commit()
        flash('Message sent successfully!', 'success')
        return redirect(url_for('messages.inbox'))
    
    return render_template('messages/send_message.html', form=form, receiver=receiver)

@messages_bp.route('/conversation/<int:other_user_id>', methods=['GET', 'POST'])
@login_required
def conversation(other_user_id):
    other_user = User.query.get_or_404(other_user_id)
    if other_user == current_user:
        flash('You cannot have a conversation with yourself.', 'warning')
        return redirect(url_for('messages.inbox'))
    
    # Fetch all messages between the current user and the other user
    messages = Message.query.filter(
        (Message.sender_id == current_user.id) & (Message.receiver_id == other_user_id) |
        (Message.sender_id == other_user_id) & (Message.receiver_id == current_user.id)
    ).order_by(Message.timestamp.asc()).all()
    
    form = MessageForm()
    if form.validate_on_submit():
        # Send a new message as part of the conversation
        new_message = Message(
            sender_id=current_user.id,
            receiver_id=other_user.id,
            content=form.content.data
        )
        db.session.add(new_message)
        db.session.commit()
        flash('Message sent!', 'success')
        return redirect(url_for('messages.conversation', other_user_id=other_user.id))

    return render_template('messages/conversation.html', messages=messages, form=form, other_user=other_user)


@messages_bp.route('/inbox', methods=['GET'])
@login_required
def inbox():
    messages = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.timestamp.desc()).all()
    return render_template('messages/inbox.html', messages=messages)

@messages_bp.route('/sent', methods=['GET'])
@login_required
def sent_messages():
    messages = Message.query.filter_by(sender_id=current_user.id).order_by(Message.timestamp.desc()).all()
    return render_template('messages/sent_messages.html', messages=messages)
