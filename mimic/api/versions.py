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

import webob.dec
import webob.exc

from mimic.openstack.common import wsgi


class Versions(object):

    @classmethod
    def factory(cls, global_config, **local_config):
        return cls()

    @webob.dec.wsgify(RequestClass=wsgi.Request)
    def __call__(self, req):
        """Return all mimic API versions."""
        version_objs = [
            {
                "id": "v1.0",
                "status": "CURRENT",
            },
        ]
        if req.path != '/':
            return webob.exc.HTTPNotFound()

        reponse_data = dict(versions=version_objs)
        content_type = req.best_match_content_type()
        serializer = wsgi.ResponseSerializer()

        return serializer.serialize(reponse_data, content_type)
