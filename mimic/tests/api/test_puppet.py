"""
Tests for the API /puppets/ methods.
"""

import mock
import commands
import subprocess

from mimic.tests.api import base
from mimic.engine import manager


class TestListPuppets(base.FunctionalTest):

    def setUp(self):
        super(TestListPuppets, self).setUp()

    def test_many(self):
        puppets = self.get_json("/puppets")
        for puppet in puppets:
            self.assertEqual(puppet['status'], False)

    def test_put(self):
        content = {
            "service": "os-preinstall",
            "status": True
        }
        self.put_json("/puppets", content)
        puppets = self.get_json("/puppets")
        for puppet in puppets:
            if puppet['service'] == "os-preinstall":
                self.assertEqual(puppet['status'], True)

    def test_create(self):
        commands.getstatusoutput = mock.MagicMock(return_value=(True, "test"))
        subprocess.Popen = mock.MagicMock(return_value=None)
        manager.build_host_data = mock.MagicMock(return_value=None)
        response = self.post_json("/puppets", {})
        self.assertEqual(response.status_int, 200)
