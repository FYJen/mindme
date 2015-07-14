import json
from flask import request

from app import mindme_api
from lib import status


@mindme_api.route('/api/v1/reminder/get/', methods=['GET'])
def reminder_get():
    return 'reminder_find'


@mindme_api.route('/api/v1/reminder/create', methods=['POST'])
def reminder_create():
    return 'reminder_create'


@mindme_api.route('/api/v1/reminder/update', methods=['POST'])
def reminder_update():
    return 'reminder_update'
