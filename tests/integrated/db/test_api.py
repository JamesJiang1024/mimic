import datetime
import unittest

from faucet.common import config
from faucet.common import context
from faucet.common import exception
from faucet import db
from faucet.db.sqlalchemy import session


class DBApiTestCase(unittest.TestCase):

    def setUp(self):
        super(DBApiTestCase, self).setUp()
        import pdb; pdb.set_trace()
        engine = session.get_engine()
        self.connection = engine.connect()
        #self.context = context.get_context()

    def tearDown(self):
        pass

    def truncate_table(self, table):
        execution = self.connection.execution_options(autocommit=True)
        execution.execute("TRUNCATE %s;" % table)

    def truncate_all_tables(self):
        self.truncate_table('vips')
        self.truncate_table('devices')
        self.truncate_table('pools')
        self.truncate_table('monitors')
        self.truncate_table('nodes')

    def compare_records(self, expect, actual, skiped=None):
        for k, v in actual.__dict__.iteritems():
            if k.startswith('_') or k in skiped:
                continue
            elif isinstance(v, datetime.datetime):
                continue
            self.assertEqual(expect[k], v)

    def test_vip_create(self):
        self.truncate_all_tables()
        print "just a test"
        pass
        expect = db.vip_create(self.context, xxx)
        actual = db.vip_get(self.context, expect.id)
        self.compare_records(expect, actual, skiped=['id'])


if __name__ == '__main__':
    unittest.main()
