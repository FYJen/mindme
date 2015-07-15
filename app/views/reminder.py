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
    # TODO(ajen): Remove testing and update it with actual code.
    try:
        message = Reminder.create(
            'Testing reminder create with dummy data',
            'some_fb_id_2',
            'some_fb_id_1'
        )
        result = status.HTTPOk(result=message)
    except status.CustomStatus as e:
        result = e
    except Exception:
        result = status.InternalServerError()

    return json.dumps(result.toDict())


@mindme_api.route('/api/v1/reminder/update', methods=['POST'])
def reminder_update():
    return 'reminder_update'
