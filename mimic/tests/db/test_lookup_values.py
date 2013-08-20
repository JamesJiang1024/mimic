#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from mimic.tests.db import base
from mimic.db import api as dbapi
from mimic.tests.db import utils


class DbLookupValueTestCase(base.DbTestCase):

    def setUp(self):
        super(DbLookupValueTestCase, self).setUp()
        self.dbapi = dbapi.get_instance()

    def _create_test_lookup_value(self, **kwargs):
        c = utils.get_test_lookup_value(**kwargs)
        self.dbapi.create_lookup_value(c)
        return c

    def test_create_lookup_value(self):
        self._create_test_lookup_value()

    def test_update_lookup_value(self):
        c = self._create_test_lookup_value()
        res = self.dbapi.get_lookup_value(c['id'])

        old_match = c['match']
        new_match = 'fqdn=xxx'
        self.assertNotEqual(old_match, new_match)

        res = self.dbapi.update_lookup_value(c['id'], {'match': new_match})
        self.assertEqual(new_match, res['match'])
