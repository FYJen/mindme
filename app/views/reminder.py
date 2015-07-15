import json
from flask import request

from app import mindme_api
from lib import status
from resources import Reminder


@mindme_api.route('/api/v1/reminder/get/<int:reminder_id>', methods=['GET'])
def reminder_get(reminder_id):
    try:
        message = Reminder.get(reminder_id)
        result = status.HTTPOk(result=message)
    except status.CustomStatus as e:
        result = e
    except Exception:
        result = status.InternalServerError()

    return json.dumps(result.toDict())


@mindme_api.route('/api/v1/reminder/create', methods=['POST'])
def reminder_create():
    return 'reminder_create'


@mindme_api.route('/api/v1/reminder/update', methods=['POST'])
def reminder_update():
    return 'reminder_update'
