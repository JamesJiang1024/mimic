#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from mimic.cmd import log_daemon
from mimic.tests import base
import mock

fake_input = {
    "Applying configuration": "uos-preinstall",
    "Finished catalog run": "uos-cleanup",
    "nova-api ensure changed 'stopped' to 'running'": "nova-api"
}


class LogDaemonTestCase(base.TestCase):

    def setUp(self):
        super(LogDaemonTestCase, self).setUp()

    def test_get_status_from_input(self):

        for line in fake_input:
            log_daemon.send_status = mock.MagicMock(
                return_value={"service": fake_input[line], "status": True})

            status_input_data = log_daemon.get_status_from_input(line)

            log_daemon.send_status.assert_called_with(fake_input[line])

            self.assertEqual(status_input_data,
                             {"service": fake_input[line], "status": True})
