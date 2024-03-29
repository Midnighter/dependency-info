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


"""Test the deprecated compatibility functions."""


import pytest

from depinfo import print_dependencies, show_versions


def test_print_dependencies(capsys) -> None:
    """Expect all printed information in order."""
    with pytest.deprecated_call():
        print_dependencies("depinfo")
    captured = capsys.readouterr()
    lines = captured.out.split("\n")

    assert lines[1].startswith("Package Information")
    assert lines[2].startswith("-------------------")
    assert lines[3].startswith("depinfo")

    assert lines[5].startswith("Dependency Information")
    assert lines[6].startswith("----------------------")

    assert any(line.startswith("pip") for line in lines[7:])
    assert any(line.startswith("setuptools") for line in lines[7:])
    assert any(line.startswith("wheel") for line in lines[7:])

    assert any(line.startswith("Build Tools Information") for line in lines[7:])
    assert any(line.startswith("Platform Information") for line in lines[7:])


def test_show_versions(capsys) -> None:
    """Expect all printed information in order."""
    with pytest.deprecated_call():
        show_versions()
    captured = capsys.readouterr()
    lines = captured.out.split("\n")

    assert lines[1].startswith("Package Information")
    assert lines[2].startswith("-------------------")
    assert lines[3].startswith("depinfo")

    assert lines[5].startswith("Dependency Information")
    assert lines[6].startswith("----------------------")

    assert any(line.startswith("pip") for line in lines[7:])
    assert any(line.startswith("setuptools") for line in lines[7:])
    assert any(line.startswith("wheel") for line in lines[7:])

    assert any(line.startswith("Build Tools Information") for line in lines[7:])
    assert any(line.startswith("Platform Information") for line in lines[7:])
