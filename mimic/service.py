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

from mimic.openstack.common import cfg
from mimic.openstack.common import wsgi

from mimic.common import config


class Service(object):
    """Service object for binaries running on this hosts."""

    def __init__(self, host):
        self.host = host
        self.timers = []

    def _get_manager(self):
        """Initialize a manager class for this service."""
        pass

    def start(self):
        pass

    def stop(self):
        self.timers = []

    def wait(self):
        pass


class WSGIService(object):
    """Provides ablitity to launch API from a 'paste' configuration."""

    def __init__(self, name, loader=None):
        """Initialize, but do not start the WSGI service."""
        self.name = name
        self.app = config.load_paste_app(name)
        self.service = wsgi.Service(self.app,
                                    cfg.CONF.api_listen_port,
                                    cfg.CONF.api_listen)

    def start(self):
        """Start serving this service using loaded configuration."""
        config.show_configs()
        self.service.start()

    def stop(self):
        """Stop serving this API."""
        self.service.stop()

    def wait(self):
        """Wait for the service to stop serving this API."""
        self.service.wait()
