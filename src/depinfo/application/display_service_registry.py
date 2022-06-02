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


"""Provide a display service registry."""


from typing import Type

from .abstract_display_service import AbstractDisplayService
from .display_format import DisplayFormat


class DisplayServiceRegistry:
    """Define a registry that returns display service classes based on given type."""

    @classmethod
    def display_service(
        cls, display_format: DisplayFormat
    ) -> Type[AbstractDisplayService]:
        """Return a display service class based on the given display format."""
        if display_format is DisplayFormat.Simple:
            from depinfo.infrastructure.application import SimpleDisplayService

            return SimpleDisplayService
        elif display_format is DisplayFormat.Markdown:
            from depinfo.infrastructure.application import MarkdownTableDisplayService

            return MarkdownTableDisplayService
        else:
            raise ValueError(f"Unknown display format {display_format}.")
