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


"""Provide a service that displays dependency information as simple tables."""


from operator import itemgetter
from typing import List, Tuple

from depinfo.application import AbstractDisplayService
from depinfo.domain import DependencyReport


class SimpleDisplayService(AbstractDisplayService):
    """Define a service that displays dependency information as simple tables."""

    @classmethod
    def display(cls, report: DependencyReport, max_depth: int = 1, **kwargs) -> None:
        """
        Display a dependency report to a desired maximum depth as simple tables.

        Args:
            report: A dependency report instance.
            max_depth:  The maximum desired depth (default 1).
            **kwargs: Keyword arguments are ignored.

        """
        print(
            "\n".join(
                [
                    "",
                    "Platform Information",
                    "--------------------",
                    *cls._format_pairs(
                        [
                            (report.platform.name, report.platform.version),
                            (report.python.name, report.python.version),
                        ]
                    ),
                ]
            )
        )
        requirements = sorted(
            report.iter_unique_requirements(
                missing_version="missing", max_depth=max_depth
            ),
            key=itemgetter(0),
        )
        print(
            "\n".join(
                [
                    "",
                    "Dependency Information",
                    "----------------------",
                    *cls._format_pairs(requirements),
                ]
            )
        )
        print(
            "\n".join(
                [
                    "",
                    "Build Tools Information",
                    "-----------------------",
                    *cls._format_pairs(
                        sorted(
                            (
                                (pkg.name, pkg.version)
                                for pkg in report.build_tools
                                if pkg.version is not None
                            ),
                            key=itemgetter(0),
                        )
                    ),
                ]
            )
        )

    @classmethod
    def _format_pairs(cls, pairs: List[Tuple[str, str]]) -> List[str]:
        """Format pairs as two fixed width, left- and right-aligned columns."""
        max_len_name = max((len(pair[0]) for pair in pairs))
        max_len_version = max((len(pair[1]) for pair in pairs))
        return [
            f"{name:<{max_len_name}} {version:>{max_len_version}}"
            for name, version in pairs
        ]
