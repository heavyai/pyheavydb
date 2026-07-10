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

    with pytest.raises(TypeError, match="can't modify immutable instance"):
        err.error_msg = 'changed'


def test_tdb_exception_allows_python_exception_notes():
    err = TDBException('server error')

    # BaseException.add_note() writes __notes__ on Python 3.11+.
    err.add_note('first note')

    assert err.__notes__ == ['first note']


def test_tdb_exception_can_propagate_through_contextlib():
    @contextmanager
    def passthrough():
        yield

    # contextlib re-raises through BaseException state; the generated
    # immutable __setattr__ used to mask TDBException with TypeError here.
    with pytest.raises(TDBException, match='server error'):
        with passthrough():
            raise TDBException('server error')
