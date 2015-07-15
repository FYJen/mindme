from app import db
from base import API_Base
from dbmodels import models
from datetime import datetime
from lib import status


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
    def create(cls, text, author_fb_id, assignee_fb_id):
        # TODO(ajen): Update status_id.
        message = models.Message(
            message=text,
            date=datetime.now(),
            status_id=3
        )
        db.session.add(message)

        assignee = models.User.query.filter_by(fb_id=assignee_fb_id).first()
        if not assignee:
            raise status.ResourceNotFound(
                details='Given assignee_fb_id %s is not found.' % assignee_fb_id
            )

        author = models.User.query.filter_by(fb_id=author_fb_id).first()
        if not assignee:
            raise status.ResourceNotFound(
                details='Given author_fb_id %s is not found.' % assignee_fb_id
            )

        rcv_user_mapping = models.ReceivedMessage(
            user_id=assignee.id,
            message=message,
        )
        db.session.add(rcv_user_mapping)

        sent_user_mapping = models.SentMessage(
            user_id=author.id,
            message=message,
        )
        db.session.add(sent_user_mapping)

        db.session.commit()

        return 'Reminder - "%s" created' % truncate_str(text)

    @classmethod
    def _to_Dict(cls, message, deref_all, *args, **kwargs):
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
