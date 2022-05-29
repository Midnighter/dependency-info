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


"""Provide a display service factory."""


from enum import Enum, auto
from typing import Type

from depinfo.application import AbstractDisplayService


class AutoNameEnum(Enum):
    """Define an enumeration base class whose fields' names match the values."""

    @staticmethod
    def _generate_next_value_(name: str, _, __, ___) -> str:
        """Use a field's name as its value."""
        return name


class DisplayType(AutoNameEnum):
    """Define an enumeration for supported display methods."""

    Simple = auto()
    Markdown = auto()
    Textual = auto()


class DisplayServiceRegistry:
    """Define a registry that returns display service classes based on given values."""

    @classmethod
    def display_service(cls, display: DisplayType) -> Type[AbstractDisplayService]:
        """Return a display service class based on the given display type value."""
        if display is DisplayType.Simple:
            from .simple_display_service import SimpleDisplayService

            return SimpleDisplayService
        elif display is DisplayType.Markdown:
            from .markdown_table_display_service import MarkdownTableDisplayService

            return MarkdownTableDisplayService
        else:
            raise ValueError(f"Unknown display type {display}.")
