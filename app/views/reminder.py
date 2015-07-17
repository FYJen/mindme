from flask import request
from flask import jsonify

from app import mindme_api
from lib import status as custom_status
from resources import Reminder


@mindme_api.route('/api/v1/reminder/get/<int:reminder_id>/', methods=['GET'])
def reminder_get(reminder_id):
    try:
        message = Reminder.get(reminder_id)
        result = custom_status.HTTPOk(result=message)
    except custom_status.CustomStatus as e:
        result = e
    except Exception:
        result = custom_status.InternalServerError()

    result = result.toDict()
    resp = jsonify(result)
    resp.status_code = result['status']['statusCode']

    return resp


@mindme_api.route('/api/v1/reminder/create/', methods=['POST'])
def reminder_create():
    query_args = {
        'message': request.args.get('message', ''),
        'author_id': request.args.get('author_id', None),
        'assignee_id': request.args.get('assignee_id', None)
    }

    try:
        message = Reminder.create(**query_args)
        result = custom_status.HTTPOk(result=message)
    except custom_status.CustomStatus as e:
        result = e
    except Exception:
        result = custom_status.InternalServerError()

    result = result.toDict()
    resp = jsonify(result)
    resp.status_code = result['status']['statusCode']

    return resp


@mindme_api.route('/api/v1/reminder/update/', methods=['POST'])
def reminder_update():
    query_args = {
        'message_id': request.args.get('message_id', None),
        'new_status': request.args.get('new_status', ''),
        'message': request.args.get('message', '')
    }

    try:
        message = Reminder.update(**query_args)
        result = custom_status.HTTPOk(result=message)
    except custom_status.CustomStatus as e:
        result = e
    except Exception:
        result = custom_status.InternalServerError()

    result = result.toDict()
    resp = jsonify(result)
    resp.status_code = result['status']['statusCode']

    return resp
