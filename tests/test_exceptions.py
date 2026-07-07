# SPDX-FileCopyrightText: Copyright (c) 2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from contextlib import contextmanager

import pytest

from heavydb.thrift.ttypes import TDBException


def test_tdb_exception_allows_python_exception_state_attrs():
    err = TDBException('server error')

    err.__traceback__ = None
    err.__context__ = None
    err.__cause__ = None
    err.__suppress_context__ = False
    err.__notes__ = ['note']

    with pytest.raises(TypeError, match="can't modify immutable instance"):
        err.error_msg = 'changed'


def test_tdb_exception_allows_python_exception_notes():
    err = TDBException('server error')

    err.add_note('first note')

    assert err.__notes__ == ['first note']


def test_tdb_exception_can_propagate_through_contextlib():
    @contextmanager
    def passthrough():
        yield

    with pytest.raises(TDBException, match='server error'):
        with passthrough():
            raise TDBException('server error')
