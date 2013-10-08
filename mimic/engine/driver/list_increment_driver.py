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
from mimic.engine import foreman_helper


class ListIncrementDriver(base.BaseSmartParameter):

    def __init__(self, name, format, classes, role):
        base.BaseSmartParameter.__init__(self, name, format, classes, role)

    def action(self, count, hostname, **kwargs):
        # get action informations
        ip = kwargs['ip']
        hosts = foreman_helper.hosts()

        # init parameters
        result = ""
        selected_lookup = []

        # get value of lookup_keys and lookup_key_ids
        for host in hosts:
            hn = host['host']['name']
            lv = self.dbapi.\
                   find_lookup_value_by_id_match("fqdn=%s" % hn, self.key)[0]
            selected_lookup.append(lv.id)
            result = lv.value

        # fromat judgeing
        format_types = {"ipaddr": ip, "hostname": hostname}
        for format_type in format_types:
            if format_type in self.format:
                form = self.format.replace(format_type,
                        format_types[format_type])

        if result == "":
            result = "---"
            result += " \n - %s" % form
        else:
            result += " \n - %s" % form

        # append new ip format to old lookup_values
        for selected_lu in selected_lookup:
            lookup_values = {
                "value": str(result),
            }
            self.dbapi.update_lookup_value(selected_lu, lookup_values)

        # create a new lookup_values
        lookup_values = {
            "match": "fqdn=%s.ustack.in" % hostname,
            "value": str(result),
            "lookup_key_id": self.key
        }
        self.dbapi.create_lookup_value(lookup_values)


def get_backend(name, format, classes, role):
    return ListIncrementDriver(name, format, classes, role)
