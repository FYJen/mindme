import json
from flask import request

from app import mindme_api
from lib import status as custom_status
from resources import User


@mindme_api.route('/api/v1/user/login/', methods=['POST'])
def user_login():
    query_args = {
        'token': request.args.get('token', ''),
        'expiration': request.args.get('expiration', ''),
        'fb_id': request.args.get('fb_id', '')
    }

    try:
        user = User.login(**query_args)
        result = custom_status.HTTPOk(result=user)
    except custom_status.CustomStatus as e:
        result = e
    except Exception:
        result = custom_status.InternalServerError()

    return json.dumps(result.toDict())


@mindme_api.route('/api/v1/user/logout/', methods=['POST'])
def user_logout():
    return 'user_logout'
