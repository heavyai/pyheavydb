# SPDX-FileCopyrightText: Copyright (c) 2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import sys
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


@pytest.mark.skipif(sys.version_info < (3, 11), reason="BaseException.add_note() requires Python 3.11+")
def test_tdb_exception_allows_python_exception_notes():
    err = TDBException('server error')

    # BaseException.add_note() writes __notes__ on Python 3.11+.
    err.add_note('first note')

    assert err.__notes__ == ['first note']


def test_tdb_exception_can_propagate_through_contextlib():
    @contextmanager
    def passthrough():
        yield

    # This propagation path used to mask TDBException with TypeError
    # when generated immutable __setattr__ rejected exception-state updates.
    with pytest.raises(TDBException, match='server error'):
        with passthrough():
            raise TDBException('server error')
