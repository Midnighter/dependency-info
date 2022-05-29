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


"""Provide an abstract base class for dependency information display services."""


from abc import ABC, abstractmethod

from depinfo.domain import DependencyReport


class AbstractDisplayService(ABC):
    """Define an abstract base class for dependency information display services."""

    @classmethod
    @abstractmethod
    def display(cls, report: DependencyReport, max_depth: int = 1, **kwargs) -> None:
        """
        Display a dependency report to a desired maximum depth.

        Args:
            report: A dependency report instance.
            max_depth:  The maximum desired depth (default 1).
            **kwargs: Keyword arguments are passed on to the actual display method.

        """
