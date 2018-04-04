#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hapcat database models.
"""

from __future__ import absolute_import, with_statement, print_function

from sqlalchemy import (
    Column
)

from hapcat.types import GUID
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(GUID, primary_key=True)
    name = Column(UnicodeText, nullable=False)
