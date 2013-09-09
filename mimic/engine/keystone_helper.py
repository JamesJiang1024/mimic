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

import httplib2
from mimic.openstack.common import jsonutils

from oslo.config import cfg

keystone_opts = [
    cfg.StrOpt('admin_tenant_id',
               default='14f905713c30496d8d14ddf153216a68',
               help=('Admin Tenant ID'),
               ),
    cfg.StrOpt('admin_user_id',
               default='c4b6e154c1964313950e850af98689f2',
               help=('Admin User ID'),
               ),
    cfg.StrOpt('admin_password',
               default='admin',
               help=('Keystone Admin Password'),
             ),
    cfg.StrOpt('admin_role_id',
               default='f8a4a80076f749d9b30790999ebe937d',
               help=('Keystone Admin Role'),
             ),
    cfg.StrOpt('auth_url',
               default='http://192.168.10.11:35357/v3',
               help=('Keystone Auth Url'))
]

CONF = cfg.CONF
CONF.register_opts(keystone_opts)


def create_admin(username, password):
    token = get_token()
    create_user(token, username, password)
    return authority(token)


def create_user(token, username, password):
    post_data = {
       "user": {
       "enabled": True,
       "name": username,
       "password": password
       }
    }
    h = httplib2.Http(".cache")
    resp, content = h.request("%s/users"
                              % cfg.CONF.auth_url, "POST",
                              body=jsonutils.dumps(post_data),
                              headers={'content-type': 'application/json',
                              'X-Auth-Token': token})
    return resp, content


def authority(token):
    h = httplib2.Http(".cache")
    resp, content = h.request("%s/projects/%s/users/%s/roles/%s"
            % (CONF.auth_url, CONF.admin_tenant_id,
                CONF.admin_user_id, CONF.admin_role_id),
            "PUT", headers={'X-Auth-Token': token})
    return resp, content


def get_token():
    post_data = {
      "auth": {
        "identity": {
            "methods": [
                "password"
            ],
            "password": {
                "user": {
                    "id": cfg.CONF.admin_user_id,
                    "password": cfg.CONF.admin_password
                }
            }
         },
         "scope": {
            "project": {
              "id": cfg.CONF.admin_tenant_id
            }
         }
       }
    }
    h = httplib2.Http(".cache")
    resp, content = h.request("%s/auth/tokens"
                              % cfg.CONF.auth_url, "POST",
                              body=jsonutils.dumps(post_data),
                              headers={'content-type': 'application/json'})

    token = resp['x-subject-token']
    return token
