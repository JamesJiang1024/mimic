"""
Tests for the API /networks/ methods.
"""

import mock

from mimic.engine import foreman_helper
from mimic.tests.api import base
from mimic.engine import network_scanning as network_scan
from mimic.tests.db import utils as dbutils


class TestNetworks(base.FunctionalTest):

    def setUp(self):
        super(TestNetworks, self).setUp()
        self.dbapi.create_lookup_value(
            dbutils.get_test_lookup_value(id=1,
                                          match="env=subnet",
                                          value="192.168.10.0"))
        self.dbapi.create_lookup_value(
            dbutils.get_test_lookup_value(id=2,
                                          match="env=fixed_range",
                                          value="192.168.10.0/24"))
        self.dbapi.create_lookup_value(
            dbutils.get_test_lookup_value(id=3,
                                          match="env=netmask",
                                          value="25"))
        self.dbapi.create_lookup_value(
            dbutils.get_test_lookup_value(id=4,
                                          match="env=gateway",
                                          value="192.168.10.1"))
        self.dbapi.create_lookup_value(
            dbutils.get_test_lookup_value(id=5,
                                          match="env=master",
                                          value="192.168.10.11"))

    def test_create(self):
        data = {
            'dhcp_range': '192.168.10.0 192.168.10.99',
            'subnet': '192.168.10.0'
        }
        foreman_helper.update_subnet = mock.MagicMock(return_value=None)
        response = self.post_json('/networks', data)
        self.assertEqual(response.status_int, 200)

    def test_one(self):
        network_scan.dhcp_scan = mock.MagicMock(return_value=True)
        network_scan.gateway_scan = mock.MagicMock(return_value=True)
        data = {
            "dhcp_status": True,
            "gateway_status": True,
            "subnet_status": True
        }
        result = self.get_json('/networks/status')
        self.assertEqual(data, result)

    def test_many(self):
        network_scan.get_network_info_from_file = mock.MagicMock(return_value={
            "subnet": "192.168.10.0", "master": "192.168.10.11",
            "gateway": "192.168.10.1", "netmask": "24"})
        data = self.get_json("/networks")
        networklist = {
            u'subnet': u'192.168.10.0',
            u'netmask': 24,
            u'master': u'192.168.10.11',
            u'dhcp_range': None,
            u'gateway': u'192.168.10.1'}
        self.assertEqual(data, networklist)
