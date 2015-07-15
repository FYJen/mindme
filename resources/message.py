from dbmodels import models
from lib import status


class Reminder(object):
    """
    """

    @classmethod
    def get(cls, reminder_id, deref_all=True):
        """
        """
        message = models.Message.query.get(reminder_id)

        if not message:
            raise status.ResourceNotFound(
                msg='No message found with the given id - %s' % reminder_id
            )

        return [cls._to_Dict(msg, deref_all) for msg in [message]]

    @classmethod
    def _to_Dict(cls, message, deref_all):
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
