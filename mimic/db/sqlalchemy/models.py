# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 Sina Corporation
# All Rights Reserved.
# Author: jiangwt100 <jiangwt100@gmail.com>
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
SQLAlchemy models for mimic data.
"""
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy.ext import declarative

from mimic.openstack.common import timeutils

BASE = declarative.declarative_base()


class DictBase(object):
    """Base class for Shunt Models."""
    __table_args__ = {'mysql_engine': 'InnoDB'}
    created_at = sql.Column(sql.DateTime, default=timeutils.utcnow)
    updated_at = sql.Column(sql.DateTime, onupdate=timeutils.utcnow)
    deleted_at = sql.Column(sql.DateTime)
    deleted = sql.Column(sql.Boolean, default=False)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __iter__(self):
        self._i = iter(orm.object_mapper(self).columns)
        return self

    def next(self):
        n = self._i.next().name
        return n, getattr(self, n)

    def update(self, values):
        """Make the model object behave like a dict"""
        for k, v in values.iteritems():
            setattr(self, k, v)

    def iteritems(self):
        """Make the model object behave like a dict.
        Includes attributes from joins."""
        local = dict(self)
        joined = dict([(k, v) for k, v in self.__dict__.iteritems()
                       if not k[0] == '_'])
        local.update(joined)
        return local.iteritems()


class VIP(BASE, DictBase):
    """Represents a listener accept packet's from user."""

    __tablename__ = 'vips'
    id = sql.Column(sql.String(36), primary_key=True)
    name = sql.Column(sql.String(255), default=None)
    description = sql.Column(sql.String(255), default=None)
    address = sql.Column(sql.String(64), nullable=False)
    port = sql.Column(sql.Integer, nullable=False)
    protocol = sql.Column(sql.String(32), nullable=False)
    lb_method = sql.Column(sql.String(32), nullable=False)
    admin_state_up = sql.Column(sql.Boolean, default=True)


class Device(BASE, DictBase):
    """Represents a load balance device."""

    __tablename__ = 'devices'
    tenant_id = sql.Column(sql.String(255), nullable=False)
    id = sql.Column(sql.String(36), primary_key=True)
    name = sql.Column(sql.String(255), default=None)
    admin_state_up = sql.Column(sql.Boolean, default=True)


class Pool(BASE, DictBase):
    """Represents a server farm and lb method to use."""

    __tablename__ = 'pools'
    tenant_id = sql.Column(sql.String(255), nullable=False)
    id = sql.Column(sql.String(36), primary_key=True)
    name = sql.Column(sql.String(255), default=None)
    protocol = sql.Column(sql.String(32), nullable=False)
    lb_method = sql.Column(sql.String(32), nullable=False)
    monitors = orm.relationship("Monitor", backref=orm.backref("pool"))
    nodes = orm.relationship("Node", backref=orm.backref("pool"))


class Monitor(BASE, DictBase):
    """Represents a healthy monitor configured on a pool."""

    __tablename__ = 'monitors'
    pool_id = sql.Column(sql.String(36), sql.ForeignKey('pools.id'))
    id = sql.Column(sql.String(36), primary_key=True)
    type = sql.Column(sql.String(32), nullable=False)
    timeout = sql.Column(sql.Integer, default=10000)   # 10 seconds
    interval = sql.Column(sql.Integer, default=30000)  # 30 seconds
    active_threshold = sql.Column(sql.Integer, default=5)
    inactive_threshold = sql.Column(sql.Integer, default=2)


class Node(BASE, DictBase):
    """Represents a service run on a server."""

    __tablename__ = 'nodes'
    tenant_id = sql.Column(sql.String(255), nullable=False)
    pool_id = sql.Column(sql.String(36), sql.ForeignKey('pools.id'))
    id = sql.Column(sql.String(36), primary_key=True)
    address = sql.Column(sql.String(64), nullable=False)
    port = sql.Column(sql.Integer, nullable=False)
    weight = sql.Column(sql.Integer, default=1)
    status = sql.Column(sql.String(32), nullable=True)
    admin_state_up = sql.Column(sql.Boolean, default=True)
