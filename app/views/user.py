import json
from flask import request
from flask import jsonify

from app import mindme_api
from config import fb_access_token_expire
from lib import status as custom_status
from resources import User


@mindme_api.route('/api/v1/user/get/<int:user_id>/', methods=['GET'])
def user_get(user_id):
    """
    """
    try:
        user = User.get(user_id)
        result = custom_status.HTTPOk(result=user)
    except custom_status.CustomStatus as e:
        result = e
    except Exception:
        result = custom_status.InternalServerError()

    result = result.toDict()
    resp = jsonify(result)
    resp.status_code = result['status']['statusCode']

    return resp


@mindme_api.route('/api/v1/user/login/', methods=['POST'])
def user_login():
    query_args = {
        'token': request.args.get('token', ''),
        'expiration': request.args.get('expiration', fb_access_token_expire),
        'fb_id': request.args.get('fb_id', ''),
        # TODO(ajen):
        #   1. Update user with real gcm id.
        'gcm_id': request.args.get('gcm_id', 'tmp_gcm_id')
    }

    try:
        user = User.login(**query_args)
        result = custom_status.HTTPOk(result=user)
    except custom_status.CustomStatus as e:
        result = e
    except Exception:
        result = custom_status.InternalServerError()

    result = result.toDict()
    resp = jsonify(result)
    resp.status_code = result['status']['statusCode']

    return resp


@mindme_api.route('/api/v1/user/logout/', methods=['POST'])
def user_logout():
    query_args = {
        'token': request.args.get('token', ''),
        'fb_id': request.args.get('fb_id', '')
    }

    try:
        user = User.logout(**query_args)
        result = custom_status.HTTPOk(result=user)
    except custom_status.CustomStatus as e:
        result = e
    except Exception:
        result = custom_status.InternalServerError()

    result = result.toDict()
    resp = jsonify(result)
    resp.status_code = result['status']['statusCode']

    return resp
