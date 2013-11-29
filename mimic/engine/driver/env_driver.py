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

from mimic.engine.driver import base


class EnvDriver(base.BaseSmartParameter):

    def __init__(self, name, format, classes, role):
        base.BaseSmartParameter.__init__(self, name, format, classes, role)

    def action(self, count, hostname, **kwargs):
        strs = self.format.split(";")
        removed = ""
        for stra in strs:
            if "env=" in stra:
                passd = stra.split("=")[1]
                removed = stra
        matched_value = self.dbapi.find_lookup_value_by_match("env=%s"
                                                            % passd)[0].value
        result = self.format
        print result
        print removed
        print matched_value
        result = result.replace(removed, matched_value)
        result = result.replace(";", "")

        lookup_values = {
            "match": "fqdn=%s.ustack.in" % hostname,
            "value": result,
            "lookup_key_id": self.key
        }
        self.dbapi.create_lookup_value(lookup_values)


def get_backend(name, format, classes, role):
    return EnvDriver(name, format, classes, role)
