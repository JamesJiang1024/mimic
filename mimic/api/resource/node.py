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
import json

from mimic.api import controller
from mimic.api import foreman_helper
from mimic.api import judgement
from mimic.openstack.common import log as logging
from mimic.openstack.common import wsgi


LOG = logging.getLogger(__name__)


class Controller(controller.Controller):
    def create(self, req, **kwargs):
        content = kwargs['body']
        mac = content['mac']
        local = content['local']
        hosts_num = foreman_helper.hosts() or {}
        host_info = {
            'name': "us"+str(len(hosts_num)+1),
            'mac': mac,
            'build': True
        }
        if local == "no":
            hostgroup_id = judgement.judge_hostgroup()
        else:
            hostgroup_id = foreman_helper.host_groups()['local']

        host_info['hostgroup_id'] = hostgroup_id

        LOG.info("Server To Post: %s" % host_info)
        return json.loads(foreman_helper.create_host(host_info))

    def delete(self, req, **kwargs):
        return True


def create_resource():
    return wsgi.Resource(Controller())
