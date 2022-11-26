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


"""Provide a package name model."""


from __future__ import annotations

import re
from typing import ClassVar, Pattern


class PackageName(str):
    """Define the package name model as a value object."""

    _pep503_pattern: ClassVar[Pattern] = re.compile(r"[-_.]+")

    @classmethod
    def normalize(cls, name: str) -> PackageName:
        """
        Normalize a package's name in compliance with PEP 503.

        A name should be lowercase and one or more occurrences of hyphens, underscores,
        or dots should be replaced by a single hyphen.
        See https://peps.python.org/pep-0503/#normalized-names

        Args:
            name: The package name as written by the package authors.

        Returns:
            A PEP 503-compliant, normalized package name.

        """
        return cls(cls._pep503_pattern.sub("-", name.lower()))
