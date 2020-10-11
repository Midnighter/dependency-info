# Copyright (c) 2018, Moritz E. Beber
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


"""Verify the expected functionality of dependency information."""


import platform
from typing import Dict

import pytest

import depinfo


def test_get_sys_info() -> None:
    """Expect correct platform information."""
    blob = depinfo.get_sys_info()
    assert "OS" in blob
    assert "OS-release" in blob
    assert "Python" in blob
    assert blob["OS"] == platform.system()
    assert blob["OS-release"] == platform.release()
    assert blob["Python"] == platform.python_version()


def test_get_pkg_info() -> None:
    """Expect minimal package dependencies."""
    blob = depinfo.get_pkg_info("depinfo")
    assert "depinfo" in blob
    assert "pip" in blob
    assert "setuptools" in blob
    assert "wheel" in blob


@pytest.mark.parametrize(
    "blob, output",
    [
        pytest.param({}, "", marks=pytest.mark.raises(exception=ValueError)),
        ({"pip": "10.0.0", "wheel": "0.5"}, "pip   10.0.0\nwheel    0.5\n"),
    ],
)
def test_print_info(capsys, blob: Dict[str, str], output: str) -> None:
    """Expect stdout in order and correctly formatted."""
    depinfo.print_info(blob)
    captured = capsys.readouterr()
    assert captured.out == output


def test_print_dependencies(capsys) -> None:
    """Expect all printed information in order."""
    depinfo.print_dependencies("depinfo")
    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    assert lines[1].startswith("System Information")
    assert lines[2].startswith("==================")
    assert lines[3].startswith("OS")
    assert lines[4].startswith("OS-release")
    assert lines[5].startswith("Python")

    assert lines[7].startswith("Package Versions")
    assert lines[8].startswith("================")
    assert any(line.startswith("depinfo") for line in lines[9:])
    assert any(line.startswith("pip") for line in lines[9:])
    assert any(line.startswith("setuptools") for line in lines[9:])
    assert any(line.startswith("wheel") for line in lines[9:])


def test_show_versions(capsys) -> None:
    """Expect all printed information in order."""
    depinfo.show_versions()
    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    assert lines[1].startswith("System Information")
    assert lines[2].startswith("==================")
    assert lines[3].startswith("OS")
    assert lines[4].startswith("OS-release")
    assert lines[5].startswith("Python")

    assert lines[7].startswith("Package Versions")
    assert lines[8].startswith("================")
    assert any(line.startswith("depinfo") for line in lines[9:])
    assert any(line.startswith("pip") for line in lines[9:])
    assert any(line.startswith("setuptools") for line in lines[9:])
    assert any(line.startswith("wheel") for line in lines[9:])
