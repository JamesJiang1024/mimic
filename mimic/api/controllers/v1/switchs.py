#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 Unitedstack.
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
"""
API Controller For Switch
"""

import commands
from pecan import rest
from oslo.config import cfg

from mimic.common.wsmeext import pecan as wsme_pecan
from mimic.openstack.common import log

switch_opts = [
    cfg.StrOpt('pxe_template_dir',
               default='/etc/mimic',
               help="mimic pxe template dir"),
    cfg.StrOpt('pxe_cfg_dir',
               default='/var/lib/tftpboot/pxelinux.cfg',
               help="mimic pxe cfg dir")
]

LOG = log.getLogger(__name__)

CONF = cfg.CONF
CONF.register_opts(switch_opts)


class SwitchController(rest.RestController):
    """Version 1 API controller."""

    @wsme_pecan.wsexpose(unicode, unicode, body=unicode)
    def put(self, status):
        scanning = status['scanning']
        LOG.info("scanning machine: %s" % scanning)
        if scanning:
            commands.getstatusoutput("cat %s/pxe.template > %s/default" %
                                (CONF.pxe_template_dir, CONF.pxe_cfg_dir))
        else:
            commands.getstatusoutput("cat %s/local.template > %s/default" %
                                     (CONF.pxe_template_dir, CONF.pxe_cfg_dir))
        return status

    @wsme_pecan.wsexpose(unicode, unicode)
    def get_all(self):
        flag, answer_local = commands.getstatusoutput("cat %s/local.template"
                                                      % CONF.pxe_template_dir)
        LOG.info("local template is now: %s" % answer_local)
        flag, answer_pxe = commands.getstatusoutput("cat %s/pxe.template"
                                                      % CONF.pxe_template_dir)
        LOG.info("pxe template is now: %s" % answer_pxe)
        flag, answer_status = commands.getstatusoutput("cat %s/default"
                                                       % CONF.pxe_cfg_dir)
        LOG.info("pxe default is now: %s" % answer_status)
        result = {}
        if answer_local == answer_status:
            result = {
                "lock": False
            }
        else:
            result = {
                "lock": True
            }
        LOG.info("lock is now: %s" % result)
        return result
