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


class SimpleDisplayService(AbstractDisplayService):
    """"""

    def __init__(self, report: DependencyReport, **kwargs) -> None:
        """"""
        super().__init__(report=report, **kwargs)

    def display(self, max_depth: int = 1, **kwargs) -> None:
        """"""
        print(
            "\n".join(
                [
                    "",
                    "Platform Information",
                    "--------------------",
                    *self._format_pairs(
                        [
                            (self._report.platform.name, self._report.platform.version),
                            (self._report.python.name, self._report.python.version),
                        ]
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
                    "Dependency Information",
                    "----------------------",
                    *self._format_pairs(requirements),
                ]
            )
        )
        print(
            "\n".join(
                [
                    "",
                    "Build Tools Information",
                    "-----------------------",
                    *self._format_pairs(
                        sorted(
                            (
                                (pkg.name, pkg.version)
                                for pkg in self._report.build_tools
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
        """"""
        max_len_name = max((len(pair[0]) for pair in pairs))
        max_len_version = max((len(pair[1]) for pair in pairs))
        return [
            f"{name:<{max_len_name}} {version:>{max_len_version}}"
            for name, version in pairs
        ]

    def _iter_unique_requirements(
        self, max_depth: int = 1
    ) -> Iterator[Tuple[str, str]]:
        """"""
        seen = set()
        for _, pkg in self._report.iter_requirements(max_depth=max_depth):
            if pkg.name in seen:
                continue
            yield pkg.name, "missing" if pkg.version is None else pkg.version
            seen.add(pkg.name)
