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
from typing import ClassVar, List, Optional, Pattern, Dict

if sys.version_info < (3, 8):
    from importlib_metadata import PackageNotFoundError, distribution
else:
    from importlib.metadata import PackageNotFoundError, distribution

from .requirement import Requirement


@dataclass(frozen=True)
class Package:
    """
    Define the package model as a value object.

    A package is defined by its name, version, requirements, and extras. It can be
    constructed from its name via a convenient factory method.

    Attributes:
        name: The package name.
        version: The package version.
        requirements: The package's requirements as other packages (if any).
        extras: Requirements for extras keyed by the extra name.

    """

    name: str
    version: Optional[str]
    requirements: List[Requirement]
    extras: Dict[str, List[Requirement]]

    _extra_pattern: ClassVar[Pattern] = re.compile(
        r"extra == '(?P<extra>[-\w.]+)'", flags=re.ASCII
    )

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
        try:
            dist = distribution(name)
        except PackageNotFoundError:
            return cls(name=name, version=None, requirements=[], extras={})
        if dist.requires is None:
            # We purposely use the distribution's chosen name when available.
            return cls(name=dist.name, version=dist.version, requirements=[], extras={})
        # Parse direct and extra requirements separately.
        requirements = []
        extras = {}
        for req in dist.requires:
            tokens = req.split(";")
            for entry in tokens[1:]:
                match = cls._extra_pattern.match(entry.strip())
                if match:
                    extras.setdefault(match.group("extra"), []).append(
                        Requirement.from_requires(tokens[0])
                    )
                    break
            else:
                requirements.append(Requirement.from_requires(tokens[0]))
        # We purposely use the distribution's chosen name when available.
        return cls(
            name=dist.name,
            version=dist.version,
            requirements=requirements,
            extras=extras,
        )
