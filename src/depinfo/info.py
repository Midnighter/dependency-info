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


"""Construct and print a package's dependencies."""


import platform
from typing import Dict, Iterable, Tuple


try:
    from importlib.metadata import PackageNotFoundError, distribution, version
except ModuleNotFoundError:
    from importlib_metadata import PackageNotFoundError, distribution, version


__all__ = (
    "get_pkg_info",
    "get_sys_info",
    "print_dependencies",
    "print_info",
    "show_versions",
)


def get_sys_info() -> Dict[str, str]:
    """Return system information as a dict."""
    blob = dict()
    blob["OS"] = platform.system()
    blob["OS-release"] = platform.release()
    blob["Python"] = platform.python_version()
    return blob


def _get_package_version(requirement: str) -> Tuple[str, str]:
    """
    Return a package, version pair from a requirement description.

    Raises:
        importlib.metadata.PackageNotFoundError: If the package is not found in the
            environment.

    """
    package = requirement.split(";", 1)[0].strip()
    return package, version(package)


def get_pkg_info(
    package_name: str,
    additional: Iterable[str] = ("pip", "flit", "pbr", "poetry", "setuptools", "wheel"),
) -> Dict[str, str]:
    """Return build and package dependencies as a dict."""
    dist = distribution(package_name)
    dependencies = {package_name: dist.version}
    for requirement in dist.requires:
        try:
            pkg, ver = _get_package_version(requirement)
        except PackageNotFoundError:
            dependencies[requirement] = "not installed"
        else:
            dependencies[pkg] = ver
    for name in additional:
        try:
            pkg, ver = _get_package_version(name)
        except PackageNotFoundError:
            continue
        else:
            dependencies[pkg] = ver
    return dependencies


def print_info(info: Dict[str, str]) -> None:
    """Print an information dict to stdout in order."""
    longest_package = max(map(len, info))
    longest_version = max(map(len, info.values()))
    for name in sorted(info):
        print(f"{name:<{longest_package}} {info[name]:>{longest_version}}")


def print_dependencies(package_name: str) -> None:
    """Print the formatted information to standard out."""
    info = get_sys_info()
    print("\nSystem Information")
    print("==================")
    print_info(info)

    info = get_pkg_info(package_name)
    print("\nPackage Versions")
    print("================")
    print_info(info)


def show_versions() -> None:
    """Print dependency information for this package."""
    print_dependencies("depinfo")
