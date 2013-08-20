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


class LookupValue(Base):
    """Represents a Lookup Value."""

    __tablename__ = 'lookup_values'

    id = Column(Integer, primary_key=True)
    match = Column(String(255))
    value = Column(String(255))
    lookup_key_id = Column(Integer)
