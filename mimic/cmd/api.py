#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""The Example Service API."""

import eventlet
eventlet.monkey_patch()

import logging
import sys
from oslo.config import cfg
from eventlet import wsgi

from mimic.api import app
from mimic.common import service as mimic_service
from mimic.openstack.common import log

CONF = cfg.CONF


def main():
    # Pase config file and command line options, then start logging
    mimic_service.prepare_service(sys.argv)

    # Build and start the WSGI app
    host = CONF.mimic_api_bind_ip
    port = CONF.mimic_api_port
    LOG = log.getLogger(__name__)
    LOG.info("Serving on http://%s:%s" % (host, port))
    LOG.info("Configuration:")
    CONF.log_opt_values(LOG, logging.INFO)
    wsgi.server(eventlet.listen((host, port)), app.VersionSelectorApplication())
