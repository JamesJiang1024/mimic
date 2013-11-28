"""
Tests for the API /switchs/ methods.
"""

import mock
import commands
from mimic.tests.api import base


class TestSwitchs(base.FunctionalTest):

    def setUp(self):
        super(TestSwitchs, self).setUp()

    def test_many(self):
        commands.getstatusoutput = mock.MagicMock(return_value=(1, "pxe"))
        result = self.get_json("/switchs")
        self.assertEqual(result['lock'], False)

    def test_put(self):
        commands.getstatusoutput = mock.MagicMock(return_value=(1, "pxe"))
        result = self.put_json("/switchs", {"scanning": True})
        self.assertEqual(result.status_int, 200)
