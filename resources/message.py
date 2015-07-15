from app import db
from base import API_Base
from dbmodels import models
from datetime import datetime
from lib import status


ACTIVE_STATUS = models.Status.query.filter_by(name='active').first()


def truncate_str(input_str, length=24, replace=' ...'):
    replace_len = len(replace)
    truncated_str = input_str[:length] + replace \
        if len(input_str) > (length + replace_len) else input_str

    return truncated_str


class Reminder(API_Base):
    """
    """

    @classmethod
    def get(cls, reminder_id, deref_all=True, *args, **kwargs):
        """
        """
        message = models.Message.query.get(reminder_id)

        if not message:
            raise status.ResourceNotFound(
                details='No message found with the given id - %s' % reminder_id
            )

        return [cls._to_Dict(msg, deref_all) for msg in [message]]

    @classmethod
    def create(cls, message='', author_id=None, assignee_id=None):
        """
        """
        # Make sure we have all the parameter we want.
        if not all([message, author_id, assignee_id]):
            raise status.InvalidRequest(
                details='Bad request. Missing message, authro_id or '
                        'assignee_id'
            )

        # Get user id for assignee by using its fb id.
        assignee = models.User.query.filter_by(fb_id=assignee_id).first()
        if not assignee:
            raise status.ResourceNotFound(
                details='Given assignee_id (%s) is not found.' % assignee_id
            )

        # Get user id for author by using its fb id.
        author = models.User.query.filter_by(fb_id=author_id).first()
        if not author:
            raise status.ResourceNotFound(
                details='Given author_id (%s) is not found.' % author_id
            )

        # Create message.
        message_obj = models.Message(
            message=message,
            date=datetime.now(),
            status_id=ACTIVE_STATUS.id
        )
        db.session.add(message_obj)

        # Create receiver and message mapping.
        rcv_user_mapping = models.ReceivedMessage(
            user_id=assignee.id,
            message=message_obj,
        )
        db.session.add(rcv_user_mapping)

        # Create sender and message mapping.
        sent_user_mapping = models.SentMessage(
            user_id=author.id,
            message=message_obj,
        )
        db.session.add(sent_user_mapping)

        # Add them to database.
        db.session.commit()

        return 'Reminder - "%s" created' % truncate_str(message)

    @classmethod
    def _to_Dict(cls, message, deref_all, *args, **kwargs):
        """
        """
        reminder_dict = {
            'id': message.id,
            'message': message.message,
            'status': message.status_id,
            'date': message.date.strftime("%Y-%m-%d")
        }

        if deref_all:
            reminder_dict.update({
                'to': message.rcv_user_mapping.assignee.fb_id,
                'from': message.sent_user_mapping.author.fb_id,
                'status': message.status.name,
            })

        return reminder_dict
