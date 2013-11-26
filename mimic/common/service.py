#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# filename   : service.py
# created at : 2013-07-01 12:23:11
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from oslo.config import cfg
from mimic.openstack.common import log


global_opts = [
    cfg.ListOpt('uos_status_modules',
                default=[
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
     ]),
    cfg.StrOpt('mimic_master_server',
               default='http://localhost:9100',
               help='mimic masters host ip'),
    cfg.StrOpt('uos_install_stage2_log',
               default='/var/log/mimic/uos_install_stage2.log',
               help='UOS install log in stage2')
]

CONF = cfg.CONF
CONF.register_opts(global_opts)


def prepare_service(argv=[]):

    cfg.CONF(argv[1:], project='mimic')
    log.setup('mimic')
