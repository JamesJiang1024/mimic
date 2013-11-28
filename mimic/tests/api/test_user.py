"""
Tests for the API /users/ methods.
"""

import mock

from mimic.tests.api import base
from mimic.engine import keystone_helper


class TestListUsers(base.FunctionalTest):

    def setUp(self):
        super(TestListUsers, self).setUp()

    def test_create(self):
        keystone_helper.create_admin = mock.MagicMock(return_value=None)
        response = self.post_json(
            "/users", {"username": "root", "password": "root"})
        self.assertEqual(response.status_int, 200)
