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


from operator import itemgetter
from typing import Iterator, List, Tuple

from depinfo.application import AbstractDisplayService
from depinfo.domain import DependencyReport, Package, Platform, Python


class MarkdownTableDisplayService(AbstractDisplayService):
    """"""

    def __init__(
        self,
        report: DependencyReport,
        platform: Platform,
        python: Python,
        build_tools: List[Package],
        **kwargs,
    ) -> None:
        """"""
        super().__init__(
            report=report,
            platform=platform,
            python=python,
            build_tools=build_tools,
            **kwargs,
        )

    def display(self, max_depth: int = 1, **kwargs) -> None:
        """"""
        print(
            "\n".join(
                [
                    "",
                    "### Platform Information",
                    "",
                    *self._format_table(
                        ["", ""],
                        [
                            (self._platform.name, self._platform.version),
                            (self._python.name, self._python.version),
                        ],
                    ),
                ]
            )
        )
        requirements = sorted(
            self._iter_unique_requirements(max_depth=max_depth), key=itemgetter(0)
        )
        print(
            "\n".join(
                [
                    "",
                    "### Dependency Information",
                    "",
                    *self._format_table(["Package", "Version"], requirements),
                ]
            )
        )
        tools = sorted(
            (
                (pkg.name, pkg.version)
                for pkg in self._build_tools
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
                    *self._format_table(["Package", "Version"], tools),
                ]
            )
        )

    @classmethod
    def _format_table(
        cls, header: List[str], pairs: List[Tuple[str, str]]
    ) -> List[str]:
        """"""
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

    def _iter_unique_requirements(
        self, max_depth: int = 1
    ) -> Iterator[Tuple[str, str]]:
        """"""
        seen = set()
        for _, pkg in self._report.iter_requirements(max_depth=max_depth):
            if pkg.name in seen:
                continue
            yield pkg.name, "**missing**" if pkg.version is None else pkg.version
