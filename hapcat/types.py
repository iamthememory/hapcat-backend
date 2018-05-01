#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hapcat database model custom types.
"""

from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

import uuid
import warnings

from sqlalchemy.types import (
    CHAR,
    TypeDecorator,
)


class GUID(TypeDecorator):
    """A platform-independent GUID type.

    This uses PostgreSQL's UUID type, otherwise using CHAR(32), storing
    as stringified hex values.

    This is taken from the SQLAlchemy examples with minor modifications.
    """

    warnings.warn(
        'Replaced with sqlalchemy_utils.types.UUIDType',
        DeprecationWarning,
    )

    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PostgresUUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return '%.32x' % uuid.UUID(value).int
            else:
                # Hexstring
                return '%.32x' % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value
