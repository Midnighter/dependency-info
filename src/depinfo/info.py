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

"""Construct and print a package's dependencies."""

from __future__ import absolute_import, print_function

import platform

import pkg_resources
from pipdeptree import build_dist_index, construct_tree


__all__ = (
    "print_dependencies", "show_versions", "get_pkg_info", "get_sys_info")


def get_sys_info():
    """Return system information as a dict."""
    blob = dict()
    blob["OS"] = platform.system()
    blob["OS-release"] = platform.release()
    blob["Python"] = platform.python_version()
    return blob


def get_pkg_info(package_name,
                 additional=["pip", "flit", "pbr", "setuptools", "wheel"]):
    """Return build and package dependencies as a dict."""
    dist_index = build_dist_index(pkg_resources.working_set)
    root = dist_index[package_name]
    tree = construct_tree(dist_index)
    dependencies = {pkg.name: pkg.installed_version for pkg in tree[root]}
    # Add the initial package itself.
    root = root.as_requirement()
    dependencies[root.name] = root.installed_version
    # Retrieve information on additional packages such as build tools.
    for name in additional:
        try:
            pkg = dist_index[name].as_requirement()
            dependencies[pkg.name] = pkg.installed_version
        except KeyError:
            continue
    return dependencies


def print_info(info):
    """Print an information dict to stdout in order."""
    format_str = "{:<%d} {:>%d}" % (max(map(len, info)),
                                    max(map(len, info.values())))
    for name in sorted(info):
        print(format_str.format(name, info[name]))


def print_dependencies(package_name):
    """Print the formatted information to standard out."""
    info = get_sys_info()
    print("\nSystem Information")
    print("==================")
    print_info(info)

    info = get_pkg_info(package_name)
    print("\nPackage Versions")
    print("================")
    print_info(info)


def show_versions():
    """Print dependency information for this package."""
    print_dependencies("depinfo")
