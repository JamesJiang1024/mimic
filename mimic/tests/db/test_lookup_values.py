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

    def test_find_lookup_value(self):
        self._create_test_lookup_value(id=1, match="fqdn=abc", lookup_key_id=1)
        self._create_test_lookup_value(id=2, match="fqdn=bcd", lookup_key_id=2)
        self._create_test_lookup_value(id=3, match="fqdn=bcd", lookup_key_id=3)
        res = self.dbapi.find_lookup_value_by_match("fqdn=abc")
        self.assertEqual(res[0].id, 1)
        res = self.dbapi.find_lookup_value_by_id_match("fqdn=bcd", 3)
        self.assertEqual(res[0].lookup_key_id, 3)

    def test_update_lookup_value(self):
        c = self._create_test_lookup_value()
        res = self.dbapi.get_lookup_value(c['id'])

        old_match = c['match']
        new_match = 'fqdn=xxx'
        self.assertNotEqual(old_match, new_match)

        res = self.dbapi.update_lookup_value(c['id'], {'match': new_match})
        self.assertEqual(new_match, res['match'])
