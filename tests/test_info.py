# -*- coding: utf-8 -*-

# Copyright (c) 2018, Moritz E.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Verify the expected functionality of dependency information."""

from __future__ import absolute_import

import platform

import pytest

import depinfo.info as depi


def test_get_sys_info():
    """Expect correct platform information."""
    blob = depi.get_sys_info()
    assert blob["OS"] == platform.system()
    assert blob["OS-release"] == platform.release()
    assert blob["Python"] == platform.python_version()


def test_get_pkg_info():
    """Expect minimal package dependencies."""
    blob = depi.get_pkg_info("dependency-info")
    assert "pip" in blob
    assert "setuptools" in blob
    assert "wheel" in blob
    assert "pipdeptree" in blob


@pytest.mark.parametrize("blob, output", [
    pytest.mark.raises(({}, ""), exception=ValueError),
    ({"pip": "10.0.0", "wheel": "0.5"}, "pip   10.0.0\nwheel    0.5\n")
])
def test_print_info(capsys, blob, output):
    """Expect stdout in order and correctly formatted."""
    depi.print_info(blob)
    captured = capsys.readouterr()
    assert captured.out == output


def test_print_dependencies(capsys):
    """Expect all printed information in order."""
    depi.print_dependencies("dependency-info")
    captured = capsys.readouterr()
    lines = captured.out.split("\n")
    assert lines[1].startswith("System Information")
    assert lines[2].startswith("==================")
    assert lines[3].startswith("OS")
    assert lines[4].startswith("OS-release")
    assert lines[5].startswith("Python")

    assert lines[7].startswith("Package Versions")
    assert lines[8].startswith("================")
    assert lines[9].startswith("pip")
    assert lines[10].startswith("pipdeptree")
    assert lines[11].startswith("setuptools")
    assert lines[12].startswith("wheel")
