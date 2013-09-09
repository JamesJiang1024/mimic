# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 UnitedStack Inc.
# All Rights Reserved.
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
""" Client For Call Keystone"""

from keystoneclient.v3 import client

from oslo.config import cfg

keystone_opts = [
    cfg.StrOpt('admin_password',
               default='admin',
               help=('Keystone Admin Password'),
             ),
    cfg.StrOpt('auth_url',
               default='http://192.168.10.11:35357/v3',
               help=('Keystone Auth Url'))
]

CONF = cfg.CONF
CONF.register_opts(keystone_opts)


keystone_client = client.Client(username="admin", auth_url=CONF.auth_url,
                            project_name="admin", password=CONF.admin_password)


def create_admin(username, password):
    user = keystone_client.users.create(username, password=password)
    project = None
    role = None
    for pro in keystone_client.projects.list():
        if pro.name == "admin":
            project = pro

    for ro in keystone_client.roles.list():
        if ro.name == "admin":
            role = ro

    result = keystone_client.roles.grant(role, user=user, project=project)
    return result
