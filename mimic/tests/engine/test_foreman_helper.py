#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import contextlib
import mock
from mimic.db import api as dbapi
from mimic.tests.db import base
from mimic.tests.driver import utils
from mimic.engine import foreman_helper


class ForemanHelperTestCase(base.DbTestCase):

    def setUp(self):
        super(ForemanHelperTestCase, self).setUp()
        foreman_helper.get_remote_data = mock.MagicMock(
            return_value="test_data")
        self.dbapi = dbapi.get_instance()

    def test_operating_system(self):
        with contextlib.nested(
        mock.patch(
            "mimic.engine.foreman_helper.get_remote_data", mock.MagicMock(
            return_value=[
                {
                "operatingsystem": {
                    "id": "13",
                    "name": "BootFromLocal"
                }
                },
                {
                "operatingsystem": {
                    "id": "4",
                    "name": "UnitedStackOS"
                }
                }
            ]
        ))):
            self.assertEqual(foreman_helper.operating_system(), ("13", "4"))

    def test_host_groups(self):
        with contextlib.nested(
            mock.patch("mimic.engine.foreman_helper.get_remote_data",
                       mock.MagicMock(
                return_value=[
                {
                "hostgroup": {
                    "id": "13",
                    "name": "master"
                }
                },
                {
                "hostgroup": {
                    "id": "4",
                    "name": "compute"
                }
                }
                ]
            ))
        ):
            data = foreman_helper.host_groups()
            print data

    def test_hosts(self):
        foreman_helper.hosts()

    def test_build_pxe_default(self):
        foreman_helper.build_pxe_default()

    def test_host_detail(self):
        foreman_helper.host_detail(11)

    def test_unused_ip(self):
        with contextlib.nested(
            mock.patch("mimic.engine.foreman_helper.get_remote_data",
                       mock.MagicMock(return_value={"ip": "192.168.10.3"})),
            mock.patch("mimic.db.api.get_instance",
                       mock.MagicMock(return_value=utils.FakeDBAPI()))
        ):
            foreman_helper.unused_ip("00:11:22:33:44:55")

    def test_create_host(self):
        foreman_helper.create_host("data")

    def test_update_subnet(self):
        foreman_helper.update_subnet(
            "192.168.10.0",
            "192.168.10.1",
            "192.168.10.12 192.168.66",
            "192.168.10.11")
