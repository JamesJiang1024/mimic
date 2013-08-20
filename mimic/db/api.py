#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# filename   : api.py<2>
# created at : 2013-07-01 21:09:07


import abc

from mimic.openstack.common.db import api as dbapi

_BACKEND_MAPPING = {'sqlalchemy': 'mimic.db.sqlalchemy.api'}
IMPL = dbapi.DBAPI(backend_mapping=_BACKEND_MAPPING)


def get_instance():
    """Return a DB API instance."""
    return IMPL


class Connection(object):
    """Base db class."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        """Constructor"""

    @abc.abstractmethod
    def create_lookup_value(self, values):
        """Create a lookup_value

        :param values: values of a lookup_value
        """

    @abc.abstractmethod
    def update_lookup_value(self, lookup_value, values):
        """Update a lookup_value

        :param lookup_value: id of a lookup_value
        :param values: value of a lookup_value
        """

    @abc.abstractmethod
    def get_lookup_value(self, lookup_value):
        """get lookup_values by id of and uuid.

        :param lookup_value: uuid of the lookup_value
        :return: a lookup_value
        """
