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


"""Provide a dependency report model with requirements information."""


from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, List, Tuple

from .package import Package
from .platform import Platform
from .python import Python


@dataclass(frozen=True)
class DependencyReport:
    """
    Define a dependency report with requirements information.

    A package is defined by its name, version, and requirements. It can be constructed
    from its name via a convenient factory method.

    Attributes:
        root: The root package instance for which to follow dependencies.
        platform: A `Platform` information instance.
        python: A `Python` information instance.
        build_tools: A list of package instances which are considered build tools rather
            than direct dependencies.
        packages: A map from package names to instances.

    """

    root: Package
    platform: Platform
    python: Python
    build_tools: List[Package]
    packages: Dict[str, Package]

    @classmethod
    def from_root(
        cls,
        root: str,
        build_tools: Iterable[str],
        max_depth: int = 1,
    ) -> DependencyReport:
        """
        Return a package instance potentially with its requirements.

        A factory class method that returns a package with its name and versions, as
        well as nested requirements as packages themselves.

        Args:
            root: The distribution name of the root package.
            build_tools: A list of build packages to include.
            max_depth: The maximum desired depth of requirements nesting.

        Returns:
            A dependency report instance with potentially nested requirements.

        """
        discovered = deque([(0, root)])
        packages: Dict[str, Package] = {}
        while len(discovered) > 0:
            level, name = discovered.popleft()
            if name in packages:
                continue
            packages[name] = pkg = Package.from_name(name)
            if level < max_depth:
                discovered.extend(((level + 1, req) for req in pkg.requirements))
        tools: List[Package] = []
        for name in build_tools:
            if name in packages:
                tools.append(packages[name])
                continue
            packages[name] = pkg = Package.from_name(name)
            tools.append(pkg)
        return cls(
            root=packages[root],
            build_tools=tools,
            packages=packages,
            platform=Platform.create(),
            python=Python.create(),
        )

    def iter_requirements(self, max_depth: int = 1) -> Iterator[Tuple[int, Package]]:
        """
        Iterate over the root package's nested requirements up to a maximum depth.

        Args:
            max_depth: The maximum desired depth of requirements nesting to iterate
                over.

        Yields:
            Dependency nesting level, package pairs.

        """
        discovered = deque([(0, self.root)])
        while len(discovered) > 0:
            level, pkg = discovered.popleft()
            if level < max_depth:
                discovered.extend(
                    ((level + 1, self.packages[req]) for req in pkg.requirements)
                )
            yield level, pkg

    def iter_unique_requirements(
        self, missing_version: str = "missing", max_depth: int = 1
    ) -> Iterator[Tuple[str, str]]:
        """
        Iterate over package name, version pairs up to a maximum dependency depth.

        Args:
            missing_version: A string to replace missing version information.
            max_depth: The maximum desired depth of dependency information.

        Yields:
            Package name, version pairs.

        """
        seen = set()
        for _, pkg in self.iter_requirements(max_depth=max_depth):
            if pkg.name in seen:
                continue
            yield pkg.name, missing_version if pkg.version is None else pkg.version
            seen.add(pkg.name)
