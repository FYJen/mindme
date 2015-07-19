from datetime import datetime

from app import db
from app import gcm_client
from base import API_Base
from config import time_format
from dbmodels import models
from gcm.gcm import GCMNotRegisteredException
from gcm.gcm import GCMUnavailableException
from lib import status as custome_status

import json
import urllib2


def truncate_str(input_str, length=24, replace=' ...'):
    replace_len = len(replace)
    truncated_str = input_str[:length] + replace \
        if len(input_str) > (length + replace_len) else input_str

    return truncated_str


def gcm_send_wrapper(user, data):
    # try:
    #     canonical_id = gcm_client.plaintext_request(
    #         registration_id=user.gcm_id,
    #         data=data
    #     )
    #     if canonical_id:
    #         # Replace reg_id with canonical_id in the database
    #         user.gcm_id = canonical_id
    #         db.session.commit()
    # except GCMNotRegisteredException:
    #     # Remove this reg_id from database
    #     pass
    # except GCMUnavailableException:
    #     # Resent the message
    #     pass
    url = 'https://android.googleapis.com/gcm/send'
    apiKey = 'AIzaSyCbnmuKVwsL1B-dGb5x4n_x-r-Q3VP0pI8'

    headers = {
        'content-type': 'application/json',
        'authorization': 'key='+apiKey
    }
    fields = {
        'registration_ids': [user.gcm_id],
        'data': {
            'id': data['id']
        }
    }

    request = urllib2.Request(url, json.dumps(fields), headers)
    resp_obj = urllib2.urlopen(request)
    response = json.loads(resp_obj.read())

    result = {}  # result sent back to client
    result['statusCode'] = resp_obj.getcode()
    result['results'] = response["results"]


class Reminder(API_Base):
    """
    """

    @classmethod
    def get(cls, reminder_id, deref_all=True):
        """
        """
        message = models.Message.query.get(reminder_id)

        if not message:
            raise custome_status.ResourceNotFound(
                details='No message found with the given id - %s' % reminder_id
            )

        return cls._to_Dict(message, deref_all)

    @classmethod
    def create(
        cls,
        message='',
        author_id=None,
        assignee_id=None,
        deref_all=False
    ):
        """
        """
        # Make sure we have all the parameter we want.
        if not all([message, author_id, assignee_id]):
            raise custome_status.InvalidRequest(
                details='Bad request: Missing message, authro_id or '
                        'assignee_id'
            )

        # Get user id for assignee by using its fb id.
        assignee = models.User.query.filter_by(fb_id=assignee_id).first()
        if not assignee:
            raise custome_status.ResourceNotFound(
                details='Given assignee_id (%s) is not found.' % assignee_id
            )

        # Get user id for author by using its fb id.
        author = models.User.query.filter_by(fb_id=author_id).first()
        if not author:
            raise custome_status.ResourceNotFound(
                details='Given author_id (%s) is not found.' % author_id
            )

        # Create message.
        ACTIVE_STATUS = models.Status.query.filter_by(name='active').first()
        created_time = datetime.now()
        message_obj = models.Message(
            message=message,
            created_date=created_time,
            last_modified_date=created_time,
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

        # TODO(ajen): Add GCM integration.
        gcm_send_wrapper(
            assignee,
            cls._to_Dict(message_obj, True, to_str=True)
        )

        return cls._to_Dict(message_obj, deref_all)

    @classmethod
    def update(
        cls,
        message_id=None,
        new_status='',
        message='',
        deref_all=False
    ):
        """
        """
        if not all([message_id, any([message, new_status])]):
            raise custome_status.InvalidRequest(
                details='Bad request: Missing message_id or new_status'
            )

        message_obj = models.Message.query.get(message_id)
        if not message_obj:
            raise custome_status.ResourceNotFound(
                details='Given message id (%s) is not found' % str(message_id)
            )

        # Update message in database.
        if new_status:
            status_obj = models.Status.query.filter_by(name=new_status).first()
            if not status_obj:
                raise custome_status.ResourceNotFound(
                    details='Given new status (%s) is not a valid '
                            'status' % new_status
                )
            message_obj.status = status_obj

        if message:
            message_obj.message = message

        message_obj.last_modified_date = datetime.now()
        db.session.commit()

        # TODO(ajen): Add GCM integration.

        return cls._to_Dict(message_obj, deref_all)

    @classmethod
    def _to_Dict(cls, message, deref_all, to_str=False, *args, **kwargs):
        """
        """
        reminder_dict = {
            'id': str(message.id) if to_str else message.id,
            'message': message.message,
            'status': message.status.name,
            'created_date': message.created_date.strftime(time_format),
            'last_modified_date':
                message.last_modified_date.strftime(time_format)
        }

        if deref_all:
            reminder_dict.update({
                'to': message.rcv_user_mapping.assignee.fb_id,
                'from': message.sent_user_mapping.author.fb_id
            })

        return reminder_dict
