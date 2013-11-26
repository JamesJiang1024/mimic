"""
Tests for the API /envs/ methods.
"""

from mimic.tests.api import base
from mimic.tests.db import utils


class TestListNodes(base.FunctionalTest):

    def setUp(self):
        super(TestListNodes, self).setUp()
        self.dbapi.create_lookup_value(
            utils.get_test_lookup_value(id=1, match="env=dhcp", value="abc"))

    def test_one(self):
        data = self.get_json("/envs/dhcp")
        self.assertEqual(data, "abc")

    def test_put(self):
        self.put_json("/envs", {"key": "dhcp", "value": "cba"})
        data = self.get_json("/envs/dhcp")
        self.assertEqual(data, "cba")

    def test_create(self):
        self.post_json("/envs", {"key": "master", "value": "11"})
        data = self.get_json("/envs/master")
        self.assertEqual(data, "11")
