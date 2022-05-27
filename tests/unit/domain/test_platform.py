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


"""Test that platform information is detected as expected."""


import sys
from typing import Dict

import pytest

from depinfo.domain import Platform


@pytest.mark.parametrize("attributes", [{"name": "Linux", "version": "4.2"}])
def test_init(attributes: Dict[str, str]) -> None:
    """Test that the platform model can be initialized correctly."""
    platform = Platform(**attributes)
    for attr, value in attributes.items():
        assert getattr(platform, attr) == value


def test_create() -> None:
    """Test that the platform is detected consistently."""
    platform = Platform.create()
    assert platform.name == sys.platform.title()
    assert platform.version
