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
import tailer
import httplib2
import commands


def send_status(service):
    data = {
        "service": service,
        "status": True
    }
    h = httplib2.Http(".cache")
    resp, content = h.request("http://localhost:9100/v1/puppets", "PUT",
                              body=json.dumps(data),
                              headers={'content-type': 'application/json'})


def main():
    status_lib = [
            'tgtd',
            'nova-api',
            'nova-compute',
            'nova-network',
            'glance-api',
            'glance-registry',
            'cinder-api',
            'cinder-volume',
            'swift-account-auditor',
            'swift-container-rep',
            'swift-object',
            'ceilometer-api',
            'ceilometer-agent-central',
            'ceilometer-collector'
           ]
    commands.getstatusoutput("touch /tmp/master_puppet.log")
    for line in tailer.follow(open('/tmp/master_puppet.log')):
        if 'Applying configuration' in line:
            send_status("uos-preinstall")
        elif 'Finished catalog run' in line:
            send_status("uos-cleanup")

        for status in status_lib:
            if "ensure changed 'stopped' to 'running'" \
               in line and status in line:
                send_status(status)
