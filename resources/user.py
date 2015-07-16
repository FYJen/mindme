from datetime import datetime

from app import db
from base import API_Base
from config import time_format
from dbmodels import models
from lib import status as custome_status


class User(API_Base):
    """
    """
    @classmethod
    def get(cls):
        """
        """
        pass

    @classmethod
    def _create(cls):
        """
        """
        # TODO(ajen):
        #   1. Generate gcm_id
        #   2. Create user in our db
        pass

    @classmethod
    def login(cls):
        """
        """
        # TODO(ajen):
        #   1. If user is not in redis, add token to redis.
        pass

    @classmethod
    def logout(cls):
        """
        """
        # TODO(ajen):
        #   1. If user is in redis, invalidate the cache.
        pass

    @classmethod
    def _to_Dict(cls):
        """
        """
        pass
