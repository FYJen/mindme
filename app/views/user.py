import json
from flask import request

from app import mindme_api
from lib import status


# @mindme_api.route('/api/v1/user/create', methods=['POST'])
# def user_create():
#     return 'user_create'


@mindme_api.route('/api/v1/user/login', methods=['POST'])
def user_login():
    return 'user_login'


@mindme_api.route('/api/v1/user/logout', methods=['POST'])
def user_logout():
    return 'user_logout'
