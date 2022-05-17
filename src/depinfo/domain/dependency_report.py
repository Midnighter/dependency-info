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
from typing import Dict, Iterator, Tuple


try:
    from importlib.metadata import PackageNotFoundError, distribution, version
except ModuleNotFoundError:
    from importlib_metadata import PackageNotFoundError, distribution, version

from .package import Package


@dataclass(frozen=True, kw_only=True)
class DependencyReport:
    """
    Define a dependency report with requirements information.

    A package is defined by its name, version, and requirements. It can be constructed
    from its name via a convenient factory method.

    Attributes:

    """

    root: Package
    packages: Dict[str, Package]

    @classmethod
    def from_root(
        cls,
        root: str,
        max_depth: int = 1,
    ) -> DependencyReport:
        """
        Return a package instance potentially with its requirements.

        A factory class method that returns a package with its name and versions, as
        well as nested requirements as packages themselves.

        Args:
            root: The distribution name of the root package.
            max_depth: The maximum desired depth of requirements nesting.

        Returns:
            A package instance with potentially nested requirements.

        """
        discovered = deque([(0, root)])
        packages: Dict[str, Package] = {}
        while len(discovered) > 0:
            level, name = discovered.popleft()
            if level > max_depth:
                break
            if name in packages:
                continue
            packages[name] = pkg = Package.from_name(name)
            discovered.extend(((level + 1, req) for req in pkg.requirements))
        return cls(
            root=packages[root],
            packages=packages,
        )

    def iter_requirements(self, max_depth: int = 1) -> Iterator[Tuple[int, Package]]:
        """
        Iterate over the root package's nested requirements up to a maximum depth.

        Args:
            max_depth: The maximum desired depth of requirements nesting to iterate
                over.

        Returns:
            An iterator over level, package pairs.

        """
        discovered = deque([(0, self.root)])
        while len(discovered) > 0:
            level, pkg = discovered.popleft()
            if level > max_depth:
                break
            discovered.extend(
                (
                    (level + 1, self.packages.setdefault(req, Package.from_name(req)))
                    for req in pkg.requirements
                )
            )
            yield level, pkg
