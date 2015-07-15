from datetime import datetime

USER = {
    'user1': {
        'id': 1,
        'fb_id': 'some_fb_id_1',
        'gcm_id': 'some_gcm_id_1'
    },
    'user2': {
        'id': 2,
        'fb_id': 'some_fb_id_2',
        'gcm_id': 'some_gcm_id_2'
    }
}

STATUS = {
    'status_1': {
        'id': 1,
        'name': 'complete'
    },
    'status_2': {
        'id': 2,
        'name': 'decline'
    },
    'status_3': {
        'id': 3,
        'name': 'active'
    },
    'status_4': {
        'id': 4,
        'name': 'canceled'
    }
}

MESSAGE = {
    'msg_1': {
        'id': 1,
        'message': 'Bring my $10, thanks',
        'created_date': datetime.now(),
        'last_modified_date': datetime.now(),
        'status_id': 1
    },
    'msg_2': {
        'id': 2,
        'message': 'Bring my $20, thanks',
        'created_date': datetime.now(),
        'last_modified_date': datetime.now(),
        'status_id': 2
    },
    'msg_3': {
        'id': 3,
        'message': 'Bring my $30, thanks',
        'created_date': datetime.now(),
        'last_modified_date': datetime.now(),
        'status_id': 3
    },
    'msg_4': {
        'id': 4,
        'message': 'Bring my $40, thanks',
        'created_date': datetime.now(),
        'last_modified_date': datetime.now(),
        'status_id': 4
    }
}

SENT_MESSAGE = {
    'sm_1': {
        'id': 1,
        'user_id': 1,
        'message_id': 1
    },
    'sm_2': {
        'id': 2,
        'user_id': 2,
        'message_id': 2
    },
    'sm_3': {
        'id': 3,
        'user_id': 1,
        'message_id': 3
    },
    'sm_4': {
        'id': 4,
        'user_id': 2,
        'message_id': 4
    }
}

RECEIVED_MESSAGE = {
    'rm_1': {
        'id': 1,
        'user_id': 2,
        'message_id': 1
    },
    'rm_2': {
        'id': 2,
        'user_id': 1,
        'message_id': 2
    },
    'rm_3': {
        'id': 3,
        'user_id': 2,
        'message_id': 3
    },
    'rm_4': {
        'id': 4,
        'user_id': 1,
        'message_id': 4
    }
}
