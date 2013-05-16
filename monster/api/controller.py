# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 Sina Corporation
# All Rights Reserved.
# Author: jiangwt100 <jiangwt100@gmail.com>
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
Controller framework
"""

from monster.openstack.common import log as logging
from monster.openstack.common import wsgi


LOG = logging.getLogger(__name__)


class Controller(object):

    RESOURCE_NAME = None
    ATTRIBUTE_MAP = None

    def __init__(self):
        pass

    def verify_request(self, context, req, body):
        """verifies required attributes are in request"""
        pass

    def index(self, req, **kwargs):
        """Returns a list of the required entities"""
        return NotImplementedError()

    def show(self, req, id, **kwargs):
        """Return detailed information about the requested entity"""
        return NotImplementedError()

    def create(self, req, body=None, **kwargs):
        """Create a new instance of the requested entity"""
        return NotImplementedError()

    def update(self, req, id, body=None, **kwargs):
        """Update the specified entity's attributes"""
        return NotImplementedError()

    def delete(self, req, id, **kwargs):
        """Delete the specified entity"""
        return NotImplementedError()
