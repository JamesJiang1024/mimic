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
Enable Driver and supporting meta-classes
"""
import json
from mimic.engine.driver import base
from mimic.db import api
from mimic.engine import foreman_helper


class ListIncrementDriver(base.BaseSmartParameter):

    def __init__(self, key, format):
        self.key = key
        self.format = format
        self.dbapi = api.get_instance()

    def action(self, count, hostname, **kwargs):
        ip = kwargs['ip']
        master_id = foreman_helper.host_groups()['master']
        hosts = foreman_helper.hosts()
        result = ""
        selected_lookup = []
        for host in hosts:
            if host['host']['hostgroup_id'] == master_id:
                hn = host['host']['name']
                lv = self.dbapi.\
                        find_lookup_value_by_id_match("fqdn=%s" % hn,
                                                          self.key)[0]
                selected_lookup.append(lv.id)
                result = lv.value
        form = self.format.replace("ipaddr", ip)
        if result == "":
            result = "---"
            result += " \n - %s" % form
        else:
            result += " \n - %s" % form
        for selected_lu in selected_lookup:
            lookup_values = {
                "value": str(result),
            }
            self.dbapi.update_lookup_value(selected_lu, lookup_values)
        lookup_values = {
            "match": "fqdn=%s.ustack.in" % hostname,
            "value": str(result),
            "lookup_key_id": self.key
        }
        self.dbapi.create_lookup_value(lookup_values)


def get_backend(key, format):
    return ListIncrementDriver(key, format)
