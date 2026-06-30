# SPDX-FileCopyrightText: Copyright (c) 2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Define exceptions as specified by the DB API 2.0 spec.

Includes some helper methods for translating thrift
exceptions to the ones defined here.
"""
from heavydb.thrift.ttypes import TDBException


_EXCEPTION_STATE_ATTRS = {
    '__traceback__',
    '__context__',
    '__cause__',
    '__suppress_context__',
}


def _patch_tdb_exception_state_attrs():
    original_setattr = TDBException.__setattr__
    if getattr(original_setattr, '_heavydb_allows_exception_state', False):
        return

    def __setattr__(self, name, value):
        if name in _EXCEPTION_STATE_ATTRS:
            return BaseException.__setattr__(self, name, value)
        return original_setattr(self, name, value)

    __setattr__._heavydb_allows_exception_state = True
    TDBException.__setattr__ = __setattr__


_patch_tdb_exception_state_attrs()


class Warning(Exception):
    """Emitted for important warnings, e.g. data truncatiions"""


class Error(Exception):
    """Base class for all pymapd errors."""


class InterfaceError(Error):
    """Raised whenever you use pymapd interface incorrectly."""


class DatabaseError(Error):
    """Raised when the database encounters an error."""


class DataError(DatabaseError):
    """Raised for data processing errors like division by zero, etc."""


class OperationalError(DatabaseError):
    """Raised for non-programmer related database errors, e.g.
    an unexpected disconnect.
    """


class IntegrityError(DatabaseError):
    """Raised when the relational integrity of the database is affected."""


class InternalError(DatabaseError):
    """Raised for errors internal to the database, e.g. and invalid cursor."""


class ProgrammingError(DatabaseError):
    """Raised for programming errors, e.g. syntax errors, table already
    exists.
    """


class NotSupportedError(DatabaseError):
    """Raised when an API not supported by the database is used."""


def _translate_exception(e):
    # type: (Exception) -> Exception
    """Translate a thrift-land exception to a DB-API 2.0
    exception.
    """
    # TODO: see if there's a way to get error codes, rather than relying msgs
    if not isinstance(e, TDBException):
        return e
    if 'SQL Error' in e.error_msg:
        err = ProgrammingError
    else:
        err = Error
    return err(e.error_msg)
