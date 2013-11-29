"""
Tests for the API /nodes methods.
"""
import mock

from mimic.tests.api import base
from mimic.tests.db import utils
import contextlib


class TestListNodes(base.FunctionalTest):

    def setUp(self):
        super(TestListNodes, self).setUp()
        self.dbapi.create_lookup_value(
            utils.get_test_lookup_value(id=1, match="env=dhcp", value="abc"))

    def test_create(self):
        with contextlib.nested(
            mock.patch("mimic.engine.manager.build_host_data",
                       mock.MagicMock(return_value=None))
        ):
            content = {
                "mac": "00:11:22:33:44:55",
                "ip": "192.168.10.11",
                "local": "yes"
            }
            response = self.post_json("/nodes", content)
            self.assertEqual(response.status_int, 200)
