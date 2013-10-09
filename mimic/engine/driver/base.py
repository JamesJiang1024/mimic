# vim: tabstop=4 shiftwidth=4 softtabstop=4
# -*- encoding: utf-8 -*-
#
# Copyright 2013 Hewlett-Packard Development Company, L.P.
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
Abstract base classes for drivers.
"""

import abc
from mimic.openstack.common import importutils
from mimic.db import api


def get_instance(driver):
    return importutils.import_module("mimic.engine.driver."
                                     + driver)


class BaseSmartParameter(object):
    """Base class for all drivers
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, name, format, classes, role):
        self.role = role
        self.name = name
        self.format = format
        self.classes = classes
        self.dbapi = api.get_instance()
        self._get_lookup_key_id()

    def _get_lookup_key_id(self):
        keys = []
        self.assistant_key = None
        for classe in self.classes:
            keys = keys + self.dbapi.get_lookup_key(self.name, classe)
        if len(keys) > 0:
            self.key = keys[0]
        if len(keys) > 1:
            self.assistant_key = keys[1]

    @abc.abstractmethod
    def action(self, count, hostname, **kwargs):
        pass
