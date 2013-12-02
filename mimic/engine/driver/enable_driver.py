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

import logging
from mimic.engine.driver import base


LOG = logging.getLogger(__name__)


class EnableDriver(base.BaseSmartParameter):

    def __init__(self, name, format, classes, role):
        base.BaseSmartParameter.__init__(self, name, format, classes, role)

    def action(self, count, hostname, **kwargs):
        LOG.info("get into enable driver, count: %s, hostname: %s" %
                 (count, hostname))
        lookup_values = {
            "match": "fqdn=%s.ustack.in" % hostname,
            "value": self.format,
            "lookup_key_id": self.key
        }
        LOG.info("final lookup_values is: %s" % lookup_values)
        self.dbapi.create_lookup_value(lookup_values)


def get_backend(name, format, classes, role):
    return EnableDriver(name, format, classes, role)
