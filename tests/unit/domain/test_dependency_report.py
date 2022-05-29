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


"""Test that dependency report works as expected."""


from typing import Dict

import pytest

from depinfo.domain import DependencyReport, Package, Platform, Python


@pytest.fixture(scope="module")
def platform() -> Platform:
    """Provide a platform fixture."""
    return Platform(name="Pi", version="3.1.4")


@pytest.fixture(scope="module")
def python() -> Python:
    """Provide a Python fixture."""
    return Python(name="PyPy", version="4.2.0")


@pytest.fixture(scope="module")
def depinfo() -> Package:
    """Provide a package fixture."""
    return Package.from_name("depinfo")


@pytest.fixture(scope="module")
def report(platform: Platform, python: Python, depinfo: Package) -> DependencyReport:
    """Provide a dependency report fixture."""
    tools = ["pip", "setuptools"]
    packages = {depinfo.name: depinfo}
    for name in depinfo.requirements + tools:
        packages[name] = Package.from_name(name)
    return DependencyReport(
        root=depinfo,
        platform=platform,
        python=python,
        build_tools=[packages[name] for name in tools],
        packages=packages,
    )


@pytest.mark.parametrize(
    "attributes",
    [{"build_tools": [], "packages": {}}],
)
def test_init(
    attributes: Dict[str, str], platform: Platform, python: Python, depinfo: Package
) -> None:
    """Test that the dependency report model can be initialized correctly."""
    pkg = DependencyReport(root=depinfo, platform=platform, python=python, **attributes)
    for attr, value in attributes.items():
        assert getattr(pkg, attr) == value


def test_iter_requirements(report: DependencyReport, depinfo: Package) -> None:
    """Test that requirements can be iterated as expected."""
    assert next(report.iter_requirements(max_depth=0)) == (0, depinfo)
    assert {pkg.name for _, pkg in report.iter_requirements()}.issuperset(
        {"importlib-metadata"}
    )
    assert {pkg.name for pkg in report.build_tools}.issuperset({"pip", "setuptools"})


def test_from_root() -> None:
    """Test dependency report creation from a root name."""
    report = DependencyReport.from_root("depinfo", ("pip", "setuptools"))
    assert {pkg.name for _, pkg in report.iter_requirements(max_depth=0)}.issuperset(
        {"depinfo"}
    )
    assert {pkg.name for _, pkg in report.iter_requirements()}.issuperset(
        {"importlib-metadata"}
    )
    assert {pkg.name for pkg in report.build_tools}.issuperset({"pip", "setuptools"})
