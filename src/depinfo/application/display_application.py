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


"""Provide an application that displays dependency information."""


from typing import Iterable

from depinfo.domain import DependencyReport

from .display_format import DisplayFormat
from .display_service_registry import DisplayServiceRegistry


class DisplayApplication:
    """Define an application that displays dependency information."""

    @classmethod
    def run(
        cls,
        package_name: str,
        display_format: DisplayFormat = DisplayFormat.Simple,
        build_tools: Iterable[str] = (
            "conda",
            "flit",
            "hatch",
            "mamba",
            "pbr",
            "pip",
            "poetry",
            "setuptools",
            "wheel",
        ),
        max_depth: int = 1,
    ) -> None:
        """
        Display the given package's dependencies in the desired format.

        Args:
            package_name: The package name for which to generate dependency information.
            display_format: One of the supported display formats.
            build_tools: A list of build packages to include.
            max_depth: The maximum desired depth of requirements nesting.

        """
        report = DependencyReport.from_root(
            root=package_name,
            build_tools=build_tools,
            max_depth=max_depth,
        )
        DisplayServiceRegistry.display_service(display_format=display_format).display(
            report=report, max_depth=max_depth
        )
