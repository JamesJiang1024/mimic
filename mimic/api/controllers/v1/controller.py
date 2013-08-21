#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from mimic.api.controllers.v1 import discovered_server
from mimic.api.controllers.v1 import node
from mimic.api.controllers.v1 import env


class Controller(object):
    """Version 1 API controller root."""

    discovered_servers = discovered_server.DiscoveredServerController()
    nodes = node.NodeController()
    envs = env.EnvController()
