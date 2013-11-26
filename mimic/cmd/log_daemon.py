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
Run logger listener
"""

import json
import sys
import logging
import tailer
import httplib2
import commands

from oslo.config import cfg

from mimic.openstack.common import log
from mimic.common import service as mimic_service

LOG = log.getLogger(__name__)

CONF = cfg.CONF


def send_status(service):
    data = {
        "service": service,
        "status": True
    }
    h = httplib2.Http(".cache")
    resp, content = h.request("%s/v1/puppets" %
                              CONF.mimic_master_server,
                              "PUT",
                              body=json.dumps(data),
                              headers={'content-type': 'application/json'})
    return data


def get_status_from_input(line):
    LOG.debug("mimic log service scanning line: %s" % line)
    if 'Applying configuration' in line:
        LOG.info("mimic log service find status: pre install")
        return send_status("uos-preinstall")
    elif 'Finished catalog run' in line:
        LOG.info("mimic log service find status: clean up")
        return send_status("uos-cleanup")

    for status in CONF.uos_status_modules:
        if "ensure changed 'stopped' to 'running'" \
           in line and status in line:
            LOG.info("mimic log service find status: %s is ok" % status)
            return send_status(status)


def main():  # pragma: no cover
    mimic_service.prepare_service(sys.argv)
    CONF.log_opt_values(LOG, logging.INFO)
    LOG.info("mimic log service start, scanning %s." %
             CONF.uos_install_stage2_log)
    commands.getstatusoutput("touch %s" % CONF.uos_install_stage2_log)
    for line in tailer.follow(open(CONF.uos_install_stage2_log)):
        get_status_from_input(line)
