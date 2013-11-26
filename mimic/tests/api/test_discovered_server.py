import mock
import webtest.app

from mimic.common import exception
from mimic.openstack.common import uuidutils
from mimic.tests.api import base
from mimic.tests.api import utils


class TestListDiscoveredServer(base.FunctionalTest):

    def setUp(self):
        super(TestListDiscoveredServer, self).setUp()
        self.machines = []
        for i in (0, 3):
           self.post_json('/discovered_servers', utils.get_machine(str(i), str(i)))
           self.machines.append(utils.get_machine(str(i), str(i)))

    def test_detail(self):
        for m in self.machines:
            self.get_json('/discovered_servers')

            data = self.get_json('/discovered_servers/%s' % m['uuid'])['data']
            self.assertEqual(m['discovered_mac'], data['discovered_mac'])

    def test_many(self):
        data = self.get_json('/discovered_servers')['data']
        for d in data:
            self.assertEqual(d['status'], 'pendding')
            self.assertEqual(d['uuid'], d['discovered_mac'])

    def test_update(self):
        self.get_json('/discovered_servers')
        self.put_json('/discovered_servers/0', {'status': 'ready'})
        data = self.get_json('/discovered_servers/0')['data']
        self.assertEqual(data['status'], 'ready')
