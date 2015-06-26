import json
from flask import request

from app import mindme_api
from lib import status


@mindme_api.route('/api/v1/reminder/', methods=['GET'])
def reminder_find():
    return 'testing'
