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

from monster.openstack.common import wsgi
from monster.openstack.common import log as logging


LOG = logging.getLogger(__name__)


##FAULT_MAP = {
##    exceptions.BadRequest: webob.exc.HTTPBadRequest,
##    exceptions.NotAuthorized: webob.exc.HTTPForbidden,
##    exceptions.NotFound: webob.exc.HTTPNotFound,
##    exceptions.ServiceUnavailable: webob.exc.HTTPServiceUnavailable,
##}


class FaultWrapper(wsgi.Middleware):

    @classmethod
    def factory(cls, global_config, **local_config):
        def _factory(app):
            return cls(app, **local_config)
        return _factory

    @webob.dec.wsgify(RequestClass=wsgi.Request)
    def __call__(self, req):
        try:
            return req.get_response(self.application)
        except Exception as ex:
            return self.handle_exception(req, ex)

    def handle_exception(self, req, ex):
        return str(ex)
