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
import logging


LOG = logging.getLogger(__name__)


class CIDRDriver(base.BaseSmartParameter):

    def __init__(self, name, format, classes, role):
        base.BaseSmartParameter.__init__(self, name, format, classes, role)

    def action(self, count, hostname, **kwargs):
        LOG.info("get into cidrdriver, count: %s, hostname: %s" %
                 (count, hostname))
        result = []
        strs = self.format.split("/")
        for stra in strs:
            matched_value = self.dbapi.find_lookup_value_by_match("env=%s"
                                                            % stra)[0].value
            LOG.debug("find match value: %s" % matched_value)
            result.append(matched_value)

        lookup_values = {
            "match": "fqdn=%s.ustack.in" % hostname,
            "value": "%s/%s" % (result[0], result[1]),
            "lookup_key_id": self.key
        }
        LOG.info("final lookup_values is: %s" % lookup_values)
        self.dbapi.create_lookup_value(lookup_values)


def get_backend(name, format, classes, role):
    return CIDRDriver(name, format, classes, role)
