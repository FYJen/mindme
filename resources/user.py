from app import db
from app import redis_store
from base import API_Base
from dbmodels import models
from lib import status as custome_status
from message import Reminder


class User(API_Base):
    """
    """
    @classmethod
    def get(cls, user_id, deref_all=True):
        """
        """
        user_obj = models.User.query.get(user_id)
        if not user_obj:
            raise custome_status.ResourceNotFound(
                details='No user found with the given id - %s' % user_id
            )

        return cls._to_Dict(user_obj, deref_all)

    @classmethod
    def _create(cls, fb_id, gcm_id):
        """
        """
        user_obj = models.User(fb_id=fb_id, gcm_id=gcm_id)

        db.session.add(user_obj)
        db.session.commit()

        return user_obj

    @classmethod
    def login(
        cls,
        token='',
        expiration='',
        fb_id='',
        gcm_id='',
        deref_all=False
    ):
        """
        """
        if not all([token, fb_id, gcm_id, expiration]):
            raise custome_status.InvalidRequest(
                details='Bad request: Missing token or fb_id'
            )

        # TODO(ajen): Perhaps we should validate fb access token. Not a big
        #             deal at the moment.

        # Check if we have the given user in our database. If not, we add it.
        user_obj = models.User.query.filter_by(fb_id=fb_id).first()
        if not user_obj:
            user_obj = cls._create(fb_id, gcm_id)

        # Set token in redis. Override it as we don't care.
        redis_store.setex(token, expiration, user_obj.fb_id)

        return cls._to_Dict(user_obj, deref_all)

    @classmethod
    def logout(cls, token='', fb_id=''):
        """
        """
        if not all([token, fb_id]):
            raise custome_status.InvalidRequest(
                details='Bad request: Missing token or fb_id'
            )

        # Invalidate the user token.
        stored_fb_id = redis_store.get(token)
        if not stored_fb_id or fb_id != stored_fb_id:
            raise custome_status.InvalidRequest(
                details='Bad request: Invalidate token'
            )

        redis_store.delete(token)

        return {}

    @classmethod
    def _to_Dict(cls, user, deref_all, *args, **kwargs):
        """
        """
        user_dict = {
            'id': user.id,
            'fb_id': user.fb_id
        }

        if deref_all:
            user_dict.update({
                'gcm_id': user.gcm_id,
                'received_messages': [
                    Reminder._to_Dict(msg.message, deref_all)
                    for msg in user.rcv_messages
                ],
                'sent_messages': [
                    Reminder._to_Dict(msg.message, deref_all)
                    for msg in user.sent_messages
                ]
            })

        return user_dict
