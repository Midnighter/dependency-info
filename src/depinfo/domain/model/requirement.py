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


"""Provide a package requirement model."""


from __future__ import annotations

from typing import Optional, NamedTuple

from .package_name import PackageName


class Requirement(NamedTuple):
    """
    Define the package requirement model as a value object.

    Attributes:
        name: The package name of the requirement.
        constraint: An optional version constraint as a string.

    """

    name: PackageName
    constraint: Optional[str] = None

    @classmethod
    def from_requires(cls, requires: str) -> Requirement:
        """
        Return a requirement instance from a requires-like string.

        The string must be shaped like the first component of the 'requires' section of
        a package distribution.

        Args:
            requires: A string giving the package name of a requirement and optionally
                a version constraint in parentheses.

        Returns:
            A requirement instance encapsulating those values.

        """
        tokens = requires.strip().split(maxsplit=1)
        return cls(
            name=PackageName.normalize(tokens[0]),
            constraint=cls._parse_constraint(tokens[1]) if len(tokens) == 2 else None,
        )

    @classmethod
    def _parse_constraint(cls, constraint: str) -> str:
        """Remove the parentheses around a constraint string."""
        return constraint.strip()[1:-1]
