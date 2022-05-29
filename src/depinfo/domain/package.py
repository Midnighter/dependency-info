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


"""Provide a package model."""


from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from typing import ClassVar, List, Optional, Pattern


if sys.version_info < (3, 8):
    from importlib_metadata import PackageNotFoundError, distribution
else:
    from importlib.metadata import PackageNotFoundError, distribution


@dataclass(frozen=True)
class Package:
    """
    Define a package model.

    A package is defined by its name, version, and requirements. It can be constructed
    from its name via a convenient factory method.

    Attributes:
        name: The package name.
        version: The package version.
        requirements: The package's requirements as other packages (if any).

    """

    name: str
    version: Optional[str]
    requirements: List[str]

    _req_pattern: ClassVar[Pattern] = re.compile(r"[\s();<>=]")

    @classmethod
    def from_name(cls, name: str) -> Package:
        """
        Return a package instance from its distribution name.

        A factory class method that returns a package with its name and version, as
        well as requirements.

        Args:
            name: A package's distribution name.

        Returns:
            A package instance with its version and requirements if it is installed in
            the current environment; otherwise only the name is set whereas the version
            and requirements are empty.

        """
        name = cls._normalize_name(name)
        try:
            dist = distribution(name)
        except PackageNotFoundError:
            result = cls(name=name, version=None, requirements=[])
        else:
            result = cls(
                name=name,
                version=dist.version,
                requirements=[]
                if dist.requires is None
                else [cls._normalize_name(cls._get_name(req)) for req in dist.requires],
            )
        return result

    @classmethod
    def _normalize_name(cls, name: str) -> str:
        """Normalize a package's name to lower case with hyphens only."""
        return name.lower().replace("_", "-")

    @classmethod
    def _get_name(cls, requirement: str) -> str:
        """
        Return the package name from requirement metadata.

        Args:
            requirement: Package requirement metadata as described in PEP 566
                (https://peps.python.org/pep-0566/).

        Returns:
            The package name.

        """
        return cls._req_pattern.split(requirement, maxsplit=1)[0]
