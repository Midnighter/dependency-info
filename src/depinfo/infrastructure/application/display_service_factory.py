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


from enum import Enum, auto

from depinfo.application import AbstractDisplayService
from depinfo.domain import DependencyReport


class AutoNameEnum(Enum):
    """"""

    @staticmethod
    def _generate_next_value_(name: str, _, __, ___) -> str:
        """"""
        return name


class DisplayType(AutoNameEnum):
    """"""

    Simple = auto()
    Markdown = auto()
    Textual = auto()


class DisplayServiceFactory:
    """"""

    @classmethod
    def create(
        cls, display: DisplayType, report: DependencyReport
    ) -> AbstractDisplayService:
        """"""
        if display is DisplayType.Simple:
            from .simple_display_service import SimpleDisplayService

            return SimpleDisplayService(report=report)
        elif display is DisplayType.Markdown:
            from .markdown_table_display_service import MarkdownTableDisplayService

            return MarkdownTableDisplayService(report=report)
        else:
            raise ValueError(f"Unknown display type {display}.")
