#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""SQLAlchemy models for App data"""

from oslo.config import cfg

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declarative_base

from mimic.openstack.common.db.sqlalchemy import models

sql_opts = [cfg.StrOpt('mysql_engine', default='InnoDB', help='MySQL engine')]
cfg.CONF.register_opts(sql_opts)


class MimicBase(models.TimestampMixin, models.ModelBase):

    metadata = None

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = self[c.name]
        return d

Base = declarative_base(cls=MimicBase)
BaseNo = declarative_base()


class LookupValue(Base):
    """Represents a Lookup Value."""

    __tablename__ = 'lookup_values'

    id = Column(Integer, primary_key=True)
    match = Column(String(255))
    value = Column(String(255))
    lookup_key_id = Column(Integer)


class LookupKey(Base):
    """Represents a Lookup Key."""

    __tablename__ = 'lookup_keys'

    id = Column(Integer, primary_key=True)
    key = Column(String(255))
    puppetclass_id = Column(Integer)
    default_value = Column(String(255))
    path = Column(String(255))
    description = Column(String(255))
    validator_type = Column(String(255))
    validator_rule = Column(String(255))
    is_param = Column(Integer)
    key_type = Column(String(255))
    override = Column(Integer)
    required = Column(Integer)
    lookup_values_count = Column(Integer)


class PuppetClasses(Base):
    """Represents a PuppetClasses."""

    __tablename__ = 'puppetclasses'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class EnvironmentClasses(BaseNo):
    """Represents a EnvironmentClasses."""

    __tablename__ = 'environment_classes'

    id = Column(Integer, primary_key=True)
    puppetclass_id = Column(Integer)
    environment_id = Column(Integer)
    lookup_key_id = Column(Integer)
