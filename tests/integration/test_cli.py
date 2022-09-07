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


"""Test the depinfo command line interface."""


import platform
from typing import List

import pytest

from depinfo.infrastructure.application.cli import main


@pytest.mark.parametrize(
    "options",
    [
        ["-h"],
        ["--help"],
    ],
)
def test_help(capsys, options: List[str]) -> None:
    """Expect the help message to be shown."""
    with pytest.raises(SystemExit) as exc:
        main(options)
    assert exc.value.code == 0

    captured = capsys.readouterr()
    assert "usage:" in captured.out
    assert "positional arguments:" in captured.out


def test_simple_format(capsys) -> None:
    """Expect the dependency information in simple format."""
    main(["depinfo"])

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


def test_markdown_format(capsys) -> None:
    """Expect the dependency information in markdown format."""
    main(["--markdown", "depinfo"])

    captured = capsys.readouterr()

    assert "### Package Information" in captured.out
    assert "| depinfo " in captured.out

    assert "### Dependency Information" in captured.out

    assert "### Build Tools Information" in captured.out
    assert "| pip " in captured.out
    assert "| setuptools " in captured.out
    assert "| wheel " in captured.out

    assert "### Platform Information" in captured.out


@pytest.mark.parametrize("depth", range(5))
def test_max_depth(depth: int) -> None:
    """Test that different dependency nesting depths can be requested."""
    main(["--max-depth", str(depth), "depinfo"])


def test_too_deep(caplog) -> None:
    """Test that there is a maximum allowed depth."""
    with pytest.raises(SystemExit) as exc:
        main(["--max-depth", str(5), "depinfo"])
    assert exc.value.code == 2

    assert any(
        msg == "The maximum depth must be >=0 and <5." for msg in caplog.messages
    )
