# vim: tabstop=4 shiftwidth=4 softtabstop=4
# -*- encoding: utf-8 -*-
#
# Copyright 2013 UnitedStack Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""
Test class for driver
"""

import mock
from mimic.db import api as dbapi
from mimic.engine.driver import local_ip_driver
from mimic.tests.db import base
from mimic.tests.driver.utils import FakeDBAPI


class LocalIpDriverTestCase(base.DbTestCase):

    def setUp(self):
        super(LocalIpDriverTestCase, self).setUp()

    def test_action(self):
        with mock.patch("mimic.db.api.get_instance",
                        mock.MagicMock(return_value=FakeDBAPI())):
                        self.dbapi = dbapi.get_instance()
                        driver = local_ip_driver.get_backend("PublicIP",
                                        "192.168.10.1",
                                        ["sunfire::masternode"],
                                        ["master"])
                        driver.action(1, "master.ustack.com", ip="192.168.10.11")
