# Copyright (c) 2022, Moritz E. Beber
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Test that Python information is detected as expected."""


import sys
from typing import Dict

import pytest

from depinfo.domain import Python


@pytest.mark.parametrize("attributes", [{"name": "PyPy", "version": "4.0.0"}])
def test_init(attributes: Dict[str, str]) -> None:
    """Test that the Python model can be initialized correctly."""
    python = Python(**attributes)
    for attr, value in attributes.items():
        assert getattr(python, attr) == value


def test_create() -> None:
    """Test that the Python version is detected consistently."""
    python = Python.create()
    assert python.name
    assert python.version == sys.version.split(maxsplit=1)[0]
