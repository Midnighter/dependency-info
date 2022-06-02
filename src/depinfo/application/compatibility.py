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


"""Provide deprecated functions for compatibility with previous versions."""


from warnings import warn

from .display_application import DisplayApplication


def print_dependencies(package_name: str) -> None:
    """Display dependency information for the given package in a simple format."""
    warn(
        DeprecationWarning(
            "The function 'print_dependencies' is deprecated since version 2.0.0. "
            "Please use either the command "
            "line interface with command 'depinfo' or import "
            "'depinfo.application.DisplayApplication' in your Python project."
        )
    )
    DisplayApplication.run(package_name=package_name)


def show_versions() -> None:
    """Display dependency information for this package in a simple format."""
    warn(
        DeprecationWarning(
            "The function 'show_versions' is deprecated since version 2.0.0. "
            "Please use either the command "
            "line interface with command 'depinfo' or import "
            "'depinfo.application.DisplayApplication' in your Python project."
        )
    )
    DisplayApplication.run(package_name="depinfo")
