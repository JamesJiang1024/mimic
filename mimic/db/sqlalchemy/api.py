#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from oslo.config import cfg

from sqlalchemy.orm.exc import NoResultFound
from mimic.common import exception
from mimic.common import utils
from mimic.db import api
from mimic.db.sqlalchemy import models
from mimic.openstack.common.db.sqlalchemy import session as db_session
from mimic.openstack.common import log
from mimic.openstack.common import uuidutils

CONF = cfg.CONF
CONF.import_opt('connection',
                'mimic.openstack.common.db.sqlalchemy.session',
                group='database')

LOG = log.getLogger(__name__)

get_engine = db_session.get_engine
get_session = db_session.get_session


def model_query(model, *args, **kwargs):
    """Query helper for simpler session usage.

    :param session: if present, the session to use
    """

    session = kwargs.get('session') or get_session()
    query = session.query(model, *args)
    return query


def get_backend():
    """The backend is this module itself."""
    return Connection()


def add_identity_filter(query, value):
    """Adds an identity filter to a query.

    Filters results by ID, if supplied value is a valid integer.
    Otherwise attempts to filter results by UUID.

    :param query: Initial query to add filter to.
    :param value: Value for filtering results by.
    :return: Modified query.
    """
    if utils.is_int_like(value):
        return query.filter_by(id=value)
    elif uuidutils.is_uuid_like(value):
        return query.filter_by(uuid=value)
    else:
        raise exception.InvalidIdentity(identity=value)


class Connection(api.Connection):

    def __init__(self):
        pass

    def create_lookup_value(self, values):
        lookup_value = models.LookupValue()
        lookup_value.update(values)
        lookup_value.save()
        return lookup_value

    def update_lookup_value(self, lookup_value, values):
        session = get_session()
        with session.begin():
            query = model_query(models.LookupValue, session=session)
            query = add_identity_filter(query, lookup_value)
            count = query.update(values, synchronize_session='fetch')
            if count != 1:
                raise exception.LookUpValueNotFound(lookup_value=lookup_value)
            ref = query.one()
        return ref

    def find_lookup_value_by_match(self, match):
        query = model_query(models.LookupValue)
        query = query.filter_by(match=match)
        return query.all()

    def find_lookup_value_by_id_match(self, match, lookup_key_id):
        query = model_query(models.LookupValue)
        query = query.filter_by(match=match)
        query = query.filter_by(lookup_key_id=lookup_key_id)
        return query.all()

    def get_lookup_value(self, lookup_value):
        query = model_query(models.LookupValue)
        query = add_identity_filter(query, lookup_value)

        try:
            result = query.one()
        except NoResultFound:
            raise exception.LookupValueNotFound(lookup_value=lookup_value)
        return result

    def _get_puppet_classes_id(self, puppet_class):  # pragma: no cover
        query = model_query(models.PuppetClasses)
        query = query.filter_by(name=puppet_class)
        return query.one()

    def get_lookup_key(self, key, puppet_class):  # pragma: no cover
        puppet_class_id = self._get_puppet_classes_id(puppet_class).id
        query = model_query(models.EnvironmentClasses.lookup_key_id)
        query = query.filter_by(puppetclass_id=puppet_class_id)
        result1 = [i[0] for i in query.all()]

        query = model_query(models.LookupKey.id)
        query = query.filter_by(key=key)
        result2 = [i[0] for i in query.all()]
        result = list(set(result1) & set(result2))
        return result
