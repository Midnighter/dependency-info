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


"""Test that package information is detected as expected."""


from typing import Dict

import pytest

from depinfo.domain import Package


@pytest.mark.parametrize(
    "attributes",
    [
        {"name": "cystalball", "version": None, "requirements": []},
        {"name": "cystalball", "version": "4.2.0", "requirements": []},
        {"name": "cystalball", "version": "4.2.0", "requirements": ["pip", "wheel"]},
    ],
)
def test_init(attributes: Dict[str, str]) -> None:
    """Test that the package model can be initialized correctly."""
    pkg = Package(**attributes)
    for attr, value in attributes.items():
        assert getattr(pkg, attr) == value


def test_from_name() -> None:
    """Test the package factory with an existing package name."""
    pkg = Package.from_name("depinfo")
    assert pkg.name == "depinfo"
    assert "importlib-metadata" in pkg.requirements


def test_missing_name() -> None:
    """Test the package factory with a missing package name."""
    pkg = Package.from_name("cystalball")
    assert pkg.name == "cystalball"
    assert pkg.version is None
    assert pkg.requirements == []
