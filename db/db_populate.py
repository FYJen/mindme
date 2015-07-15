import sys

from app import db
from app import models
from db_dummy_data import MESSAGE
from db_dummy_data import RECEIVED_MESSAGE
from db_dummy_data import SENT_MESSAGE
from db_dummy_data import STATUS
from db_dummy_data import USER

TABLES = [
    'ReceivedMessage',
    'SentMessage',
    'Message',
    'Status',
    'User'
]


class Populate(object):
    """
    """

    @classmethod
    def User(cls):
        for user in USER.values():
            u_entry = models.User(**user)
            db.session.add(u_entry)

        db.session.commit()

    @classmethod
    def Status(cls):
        for status in STATUS.values():
            s_entry = models.Status(**status)
            db.session.add(s_entry)

        db.session.commit()

    @classmethod
    def Message(cls):
        for message in MESSAGE.values():
            m_entry = models.Message(**message)
            db.session.add(m_entry)

        db.session.commit()

    @classmethod
    def SentMessage(cls):
        for sent_message in SENT_MESSAGE.values():
            sm_entry = models.SentMessage(**sent_message)
            db.session.add(sm_entry)

        db.session.commit()

    @classmethod
    def ReceivedMessage(cls):
        for received_message in RECEIVED_MESSAGE.values():
            rm_entry = models.ReceivedMessage(**received_message)
            db.session.add(rm_entry)

        db.session.commit()


class RebuildDB(object):
    """
    """

    @classmethod
    def _purgeTables(cls):
        """
        """
        for table in TABLES:
            table = getattr(models, table)
            try:
                print 'Deleting %s table ...' % table.__name__
                table.query.delete()
            except Exception:
                print 'Delete %s table ...' % table.name
                table.delete()

        db.session.commit()

    @classmethod
    def _populateTables(cls):
        for table in [
            'User',
            'Status',
            'Message',
            'SentMessage',
            'ReceivedMessage'
        ]:
            populate_table = getattr(Populate, table)
            print 'Inserting data for %s ...' % table
            populate_table()

    @classmethod
    def initialize(cls):
        cls._purgeTables()
        cls._populateTables()


def main():
    RebuildDB.initialize()
    return 0

if __name__ == '__main__':
    sys.exit(main())
