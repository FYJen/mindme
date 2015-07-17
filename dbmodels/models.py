from app import db


class ReceivedMessage(db.Model):
    """
    """
    __tablename__ = 'received_message'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message_id = db.Column(
        db.Integer,
        db.ForeignKey('message.id'),
        nullable=False
    )

    def __repr__(self):
        return '<ReceivedMessage> %r' % self.id


class SentMessage(db.Model):
    """
    """
    __tablename__ = 'sent_message'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message_id = db.Column(
        db.Integer,
        db.ForeignKey('message.id'),
        nullable=False
    )

    def __repr__(self):
        return '<SentMessage> %r' % self.id


class Message(db.Model):
    """
    """
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime)
    last_modified_date = db.Column(db.DateTime)
    status_id = db.Column(
        db.Integer,
        db.ForeignKey('status.id'),
        nullable=False
    )

    rcv_user_mapping = db.relationship(
        'ReceivedMessage',
        backref='message',
        uselist=False
    )
    sent_user_mapping = db.relationship(
        'SentMessage',
        backref='message',
        uselist=False
    )

    def __repr__(self):
        return '<Message> %r' % self.id


class Status(db.Model):
    """
    """
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    messages_with_status = db.relationship(
        'Message',
        backref='status',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<Status> %r' % self.id


class User(db.Model):
    """
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    fb_id = db.Column(db.Text, nullable=False, index=True, unique=True)
    gcm_id = db.Column(db.Text, nullable=False)

    rcv_messages = db.relationship(
        'ReceivedMessage',
        backref='assignee',
        lazy='dynamic'
    )
    sent_messages = db.relationship(
        'SentMessage',
        backref='author',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<User> %r - %r' % (self.id, self.fb_id)
