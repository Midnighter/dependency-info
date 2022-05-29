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


"""Provide a service that displays dependency information as markdown tables."""


from operator import itemgetter
from typing import List, Tuple

from depinfo.application import AbstractDisplayService
from depinfo.domain import DependencyReport


class MarkdownTableDisplayService(AbstractDisplayService):
    """Define a service that displays dependency information as markdown tables."""

    @classmethod
    def display(cls, report: DependencyReport, max_depth: int = 1, **kwargs) -> None:
        """
        Display a dependency report to a desired maximum depth as markdown tables.

        Args:
            report: A dependency report instance.
            max_depth:  The maximum desired depth (default 1).
            **kwargs: Keyword arguments are ignored.

        """
        print(
            "\n".join(
                [
                    "",
                    "### Platform Information",
                    "",
                    *cls._format_table(
                        ["", ""],
                        [
                            (report.platform.name, report.platform.version),
                            (report.python.name, report.python.version),
                        ],
                    ),
                ]
            )
        )
        requirements = sorted(
            report.iter_unique_requirements(
                missing_version="**missing**", max_depth=max_depth
            ),
            key=itemgetter(0),
        )
        print(
            "\n".join(
                [
                    "",
                    "### Dependency Information",
                    "",
                    *cls._format_table(["Package", "Version"], requirements),
                ]
            )
        )
        tools = sorted(
            (
                (pkg.name, pkg.version)
                for pkg in report.build_tools
                if pkg.version is not None
            ),
            key=itemgetter(0),
        )
        print(
            "\n".join(
                [
                    "",
                    "### Build Tools Information",
                    "",
                    *cls._format_table(["Package", "Version"], tools),
                ]
            )
        )

    @classmethod
    def _format_table(
        cls, header: List[str], pairs: List[Tuple[str, str]]
    ) -> List[str]:
        """Format pairs of information as a markdown table with two columns."""
        max_len_name = max(max((len(pair[0]) for pair in pairs)), len(header[0]))
        max_len_version = max(max((len(pair[1]) for pair in pairs)), len(header[1]))
        result = [
            f"| {header[0]:^{max_len_name}} | {header[1]:^{max_len_version}} |",
            f"|:{'-' * max_len_name}-|-{'-' * max_len_version}:|",
        ]
        result.extend(
            f"| {name:<{max_len_name}} | {version:>{max_len_version}} |"
            for name, version in pairs
        )
        return result
