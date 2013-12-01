#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import contextlib
import mock
from mimic.tests import base
from mimic.engine import network_scanning


class NetworkScanningTestCase(base.TestCase):

    def setUp(self):
        super(NetworkScanningTestCase, self).setUp()

    #def test_dhcp_scan(self):
    #    with contextlib.nested(
    #        mock.patch("scapy.all.srp",
    #                   mock.MagicMock(return_value=([], "")))):
    #    network_scanning.dhcp_scan()
